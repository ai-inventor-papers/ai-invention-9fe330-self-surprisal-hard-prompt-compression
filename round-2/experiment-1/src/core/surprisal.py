"""
Surprisal computation module for SSHPC (Self-Surprisal Hard Prompt Compression).

Computes token-level surprisal values using the target LLM's own next-token logits.
Surprisal = -log P(token_i | context up to i-1)
"""

import torch
import torch.nn.functional as F
import numpy as np
from typing import List, Optional, Tuple
from loguru import logger


class SurprisalAnalyzer:
    """Computes per-token surprisal values from a causal language model."""

    def __init__(self, model, tokenizer, device: str = "cpu"):
        self.model = model
        self.tokenizer = tokenizer
        self.device = device
        self.special_ids = set(getattr(tokenizer, 'all_special_ids', []))
        if not self.special_ids:
            # Fallback: common special token IDs for GPT-2
            self.special_ids = {tokenizer.bos_token_id, tokenizer.eos_token_id, tokenizer.pad_token_id}
            self.special_ids.discard(None)

    def compute_surprisal(self, text: str, query: Optional[str] = None) -> Tuple[List[float], List[int]]:
        """
        Compute surprisal for each token in the text.

        Args:
            text: Input text to compute surprisal for
            query: Optional query string for conditioning (QA tasks)

        Returns:
            Tuple of (surprisal_values, token_ids) for each non-special token
        """
        if query is not None:
            full_text = query + " " + text
        else:
            full_text = text

        try:
            inputs = self.tokenizer(
                full_text, return_tensors="pt",
                truncation=True, max_length=4096, padding=False,
            ).to(self.device)
        except Exception as e:
            logger.error(f"Tokenization failed: {e}")
            return [], []

        input_ids = inputs["input_ids"]
        seq_len = input_ids.shape[1]
        if seq_len < 2:
            return [], []

        try:
            with torch.no_grad():
                logits = self.model(**inputs).logits
        except Exception as e:
            logger.error(f"Model forward pass failed: {e}")
            return [], []

        shift_logits = logits[:, :-1, :].contiguous()
        shift_targets = input_ids[:, 1:].contiguous()
        log_probs = F.log_softmax(shift_logits, dim=-1)
        log_pt = log_probs.gather(-1, shift_targets.unsqueeze(-1)).squeeze(-1)
        surprisals = (-log_pt.squeeze(0)).cpu().tolist()
        token_ids = input_ids[0, 1:].cpu().tolist()

        for i, tid in enumerate(token_ids):
            if tid in self.special_ids:
                surprisals[i] = float("inf")

        return surprisals, token_ids

    def compute_token_importance(self, text: str, query: Optional[str] = None) -> List[Tuple[float, int, int]]:
        """
        Compute token importance ranked by surpral descending.
        Returns: List of (surprisal, token_id, position)
        """
        surprisals, token_ids = self.compute_surprisal(text, query)
        importance = [
            (surprisals[i], token_ids[i], i)
            for i in range(len(surprisals))
            if surprisals[i] != float("inf")
        ]
        importance.sort(key=lambda x: x[0], reverse=True)
        return importance

    def compute_perplexity(self, text: str) -> float:
        """Compute perplexity of the text using the model."""
        try:
            inputs = self.tokenizer(
                text, return_tensors="pt", truncation=True, max_length=4096
            ).to(self.device)
        except Exception:
            return float("inf")
        with torch.no_grad():
            outputs = self.model(**inputs, labels=inputs["input_ids"])
            loss = outputs.loss
        if loss is None or torch.isnan(loss):
            return float("inf")
        return float(torch.exp(loss).item())
