"""
Latency measurement module for compression evaluation.
Measures prefill and generation time.
"""

import time
import torch
from typing import Dict, Optional
from loguru import logger


def measure_latency(model, tokenizer, text: str, device: str = "cpu") -> Dict:
    """
    Measure prefill and generation latency for a model.

    Returns:
        Dict with prefill_ms, generation_ms_per_token
    """
    # Warmup
    for _ in range(3):
        try:
            inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512).to(device)
            with torch.no_grad():
                _ = model.generate(**inputs, max_new_tokens=1, do_sample=False)
        except Exception:
            pass

    # Measure prefill time
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512).to(device)

    # CUDA synchronize if available
    if device == "cuda":
        torch.cuda.synchronize()

    start = time.perf_counter()
    with torch.no_grad():
        outputs = model(**inputs)
    if device == "cuda":
        torch.cuda.synchronize()
    prefill_time = time.perf_counter() - start

    # Measure generation time per token
    max_new_tokens = min(10, 50)
    start = time.perf_counter()
    with torch.no_grad():
        generated = model.generate(**inputs, max_new_tokens=max_new_tokens, do_sample=False)
    if device == "cuda":
        torch.cuda.synchronize()
    generation_time = time.perf_counter() - start

    tokens_generated = generated.shape[1] - inputs["input_ids"].shape[1]
    gen_per_token = generation_time / max(tokens_generated, 1)

    return {
        "prefill_ms": round(prefill_time * 1000, 2),
        "generation_ms_per_token": round(gen_per_token * 1000, 2),
    }


def compute_break_even_ratio(prefill_ms: float, gen_per_token_ms: float) -> float:
    """
    Compute break-even compression ratio where prefill savings
    equal generation overhead.
    """
    if gen_per_token_ms <= 0:
        return float("inf")
    # Break-even: original_prefill = compressed_prefill + overhead
    # Simplified: ratio where saving = overhead
    return max(1.0, prefill_ms / gen_per_token_ms)


def measure_compression_latency(
    model, tokenizer, original_text: str, compressed_text: str, device: str = "cpu"
) -> Dict:
    """Measure latency for both original and compressed texts."""
    original_latency = measure_latency(model, tokenizer, original_text, device)
    compressed_latency = measure_latency(model, tokenizer, compressed_text, device)

    return {
        "original": original_latency,
        "compressed": compressed_latency,
        "prefill_savings_ms": round(original_latency["prefill_ms"] - compressed_latency["prefill_ms"], 2),
        "generation_overhead_ms": round(compressed_latency["generation_ms_per_token"] - original_latency["generation_ms_per_token"], 2),
    }