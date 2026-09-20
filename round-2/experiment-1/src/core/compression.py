"""
SSHPC compression and baseline methods implementation.
"""

import random
import torch
from typing import List, Tuple, Optional, Dict
from loguru import logger
from .surprisal import SurprisalAnalyzer


class SSHPCCompressor:
    """Self-Surprisal Hard Prompt Compression."""

    def __init__(self, analyzer: SurprisalAnalyzer):
        self.analyzer = analyzer

    def compress(self, prompt: str, target_ratio: float, query: Optional[str] = None) -> str:
        """
        Compress prompt by removing lowest-surprisal tokens.

        Args:
            prompt: Original prompt text
            target_ratio: Compression ratio (e.g., 4 means keep 1/4 of tokens)
            query: Optional query for conditioning

        Returns:
            Compressed prompt string
        """
        tokens = self.analyzer.tokenizer(prompt, add_special_tokens=False)["input_ids"]
        if len(tokens) == 0:
            return prompt

        # Compute token importance
        importance = self.analyzer.compute_token_importance(prompt, query)
        # importance is (surprisal, token_id, position)

        # Map positions to tokens
        non_special_positions = {pos: (surprisal, tid) for surprisal, tid, pos in importance}

        # Determine how many tokens to keep
        keep_count = max(1, int(len(tokens) / target_ratio))

        # Get positions of highest-surprisal tokens
        sorted_by_surprisal = sorted(importance, key=lambda x: x[0], reverse=True)
        keep_positions = set()
        for _, _, pos in sorted_by_surprisal[:keep_count]:
            keep_positions.add(pos)

        # Build compressed token list preserving order
        compressed_tokens = []
        for i, tid in enumerate(tokens):
            # Check if this is a special token (always keep)
            decoded = self.analyzer.tokenizer.decode([tid])
            if self.analyzer.tokenizer.decode([tid]).strip() == "" or tid in self.analyzer.special_ids:
                compressed_tokens.append(tid)
            elif i in keep_positions:
                compressed_tokens.append(tid)

        # Reconstruct text from tokens
        if not compressed_tokens:
            return prompt

        compressed_text = self.analyzer.tokenizer.decode(compressed_tokens, skip_special_tokens=False)
        return compressed_text

    def iterative_compress(self, prompt: str, target_ratio: float, query: Optional[str] = None, rounds: int = 3) -> str:
        """
        Iteratively re-score and prune for high compression ratios (>=8x).
        """
        current_text = prompt
        for round_idx in range(rounds):
            current_ratio = len(current_text.split()) / max(1, len(prompt.split()))
            if current_ratio <= 1.0 / target_ratio:
                break
            # Recompute surprisal on current compressed text
            current_text = self.compress(current_text, target_ratio, query)
            logger.info(f"Round {round_idx+1}: compression ratio {current_ratio:.2f}")
        return current_text


class LLMLinguaCompressor:
    """LLMLingua-style compression using GPT-2 as proxy model."""

    def __init__(self, proxy_analyzer: SurprisalAnalyzer):
        self.analyzer = proxy_analyzer

    def compress(self, prompt: str, target_ratio: float, query: Optional[str] = None) -> str:
        """
        LLMLingua: Minimum-entropy token scoring with iterative pruning.
        Uses GPT-2 as proxy model.
        """
        tokens = self.analyzer.tokenizer(prompt, add_special_tokens=False)["input_ids"]
        if len(tokens) == 0:
            return prompt

        # Compute self-information (surprisal) for each token using proxy model
        importance = self.analyzer.compute_token_importance(prompt, query)

        keep_count = max(1, int(len(tokens) / target_ratio))
        sorted_by_surprisal = sorted(importance, key=lambda x: x[0], reverse=True)
        keep_positions = set()
        for _, _, pos in sorted_by_surprisal[:keep_count]:
            keep_positions.add(pos)

        compressed_tokens = [tid for i, tid in enumerate(tokens) if i in keep_positions or tid in self.analyzer.special_ids]
        if not compressed_tokens:
            return prompt
        return self.analyzer.tokenizer.decode(compressed_tokens, skip_special_tokens=False)


class SelectiveContextCompressor:
    """SelectiveContext: GPT-2 self-information scoring."""

    def __init__(self, proxy_analyzer: SurprisalAnalyzer):
        self.analyzer = proxy_analyzer

    def compress(self, prompt: str, target_ratio: float, query: Optional[str] = None) -> str:
        """
        SelectiveContext: Score tokens by self-information and prune lowest.
        """
        tokens = self.analyzer.tokenizer(prompt, add_special_tokens=False)["input_ids"]
        if len(tokens) == 0:
            return prompt

        importance = self.analyzer.compute_token_importance(prompt, query)
        keep_count = max(1, int(len(tokens) / target_ratio))

        sorted_by_surprisal = sorted(importance, key=lambda x: x[0], reverse=True)
        keep_positions = set(pos for _, _, pos in sorted_by_surprisal[:keep_count])

        compressed_tokens = [tid for i, tid in enumerate(tokens) if i in keep_positions or tid in self.analyzer.special_ids]
        if not compressed_tokens:
            return prompt
        return self.analyzer.tokenizer.decode(compressed_tokens, skip_special_tokens=False)


class ProxyOnTargetCompressor:
    """Proxy-on-target: LLMLingua algorithm but using target LLM as proxy."""

    def __init__(self, target_analyzer: SurprisalAnalyzer):
        self.analyzer = target_analyzer

    def compress(self, prompt: str, target_ratio: float, query: Optional[str] = None) -> str:
        """
        Single-pass compression using target LLM's surprisal (no iterative conditioning).
        """
        tokens = self.analyzer.tokenizer(prompt, add_special_tokens=False)["input_ids"]
        if len(tokens) == 0:
            return prompt

        importance = self.analyzer.compute_token_importance(prompt, query)
        keep_count = max(1, int(len(tokens) / target_ratio))

        sorted_by_surprisal = sorted(importance, key=lambda x: x[0], reverse=True)
        keep_positions = set(pos for _, _, pos in sorted_by_surprisal[:keep_count])

        compressed_tokens = [tid for i, tid in enumerate(tokens) if i in keep_positions or tid in self.analyzer.special_ids]
        if not compressed_tokens:
            return prompt
        return self.analyzer.tokenizer.decode(compressed_tokens, skip_special_tokens=False)


class RandomCompressor:
    """Random token pruning baseline."""

    def __init__(self, analyzer: SurprisalAnalyzer):
        self.analyzer = analyzer

    def compress(self, prompt: str, target_ratio: float, query: Optional[str] = None) -> str:
        tokens = self.analyzer.tokenizer(prompt, add_special_tokens=False)["input_ids"]
        if len(tokens) == 0:
            return prompt

        keep_count = max(1, int(len(tokens) / target_ratio))
        # Always keep special tokens
        special_positions = {i for i, tid in enumerate(tokens) if tid in self.analyzer.special_ids}
        non_special = [i for i in range(len(tokens)) if i not in special_positions]
        random.shuffle(non_special)
        keep_positions = set(special_positions) | set(non_special[:keep_count - len(special_positions)])

        compressed_tokens = [tid for i, tid in enumerate(tokens) if i in keep_positions]
        if not compressed_tokens:
            return prompt
        return self.analyzer.tokenizer.decode(compressed_tokens, skip_special_tokens=False)


class NoCompression:
    """No-op baseline - returns original prompt."""

    def compress(self, prompt: str, target_ratio: float, query: Optional[str] = None) -> str:
        return prompt


def get_compressor(method: str, analyzer) -> object:
    """Factory function to get a compressor by name."""
    compressors = {
        "SSHPC": SSHPCCompressor(analyzer),
        "SSHPC_iterative": SSHPCCompressor(analyzer),
        "LLMLingua": LLMLinguaCompressor(analyzer),
        "SelectiveContext": SelectiveContextCompressor(analyzer),
        "Random": RandomCompressor(analyzer),
        "ProxyOnTarget": ProxyOnTargetCompressor(analyzer),
        "None": NoCompression(),
    }
    return compressors.get(method, NoCompression())


def apply_compression(prompt: str, method: str, analyzer, target_ratio: float, query: Optional[str] = None) -> str:
    """Apply compression method to a prompt."""
    compressor = get_compressor(method, analyzer)
    if method == "SSHPC_iterative":
        return compressor.iterative_compress(prompt, target_ratio, query)
    return compressor.compress(prompt, target_ratio, query)