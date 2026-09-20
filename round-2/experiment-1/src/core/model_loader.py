"""
Model loading utilities. Handles GPT-2 and other LM loading with proper error handling.
"""

import os
from typing import Optional, Tuple
from loguru import logger

# Set offline mode before any HF imports
os.environ["HF_HUB_OFFLINE"] = os.environ.get("HF_HUB_OFFLINE", "0")
os.environ["TRANSFORMERS_OFFLINE"] = os.environ.get("TRANSFORMERS_OFFLINE", "0")
os.environ["HF_DATASETS_OFFLINE"] = os.environ.get("HF_DATASETS_OFFLINE", "0")

_model_cache = {}


def load_gpt2(device: str = "cpu") -> Tuple[object, object]:
    """Load GPT-2 model and tokenizer for proxy methods. Returns (tokenizer, model)."""
    from transformers import AutoTokenizer, GPT2LMHeadModel

    logger.info("Loading GPT-2 model...")
    tokenizer = AutoTokenizer.from_pretrained("gpt2")
    model = GPT2LMHeadModel.from_pretrained("gpt2")
    model.to(device)
    model.eval()

    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    logger.info("GPT-2 loaded successfully")
    return tokenizer, model


def load_model(model_name: str, device: str = "cpu") -> Tuple[object, object]:
    """Load a model by name."""
    from transformers import AutoTokenizer, AutoModelForCausalLM

    logger.info(f"Loading model: {model_name}")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float32 if device == "cpu" else torch.float16,
        low_cpu_mem_usage=True,
    )
    model.to(device)
    model.eval()

    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    return tokenizer, model


def clear_model_cache():
    """Clear the model cache and free memory."""
    global _model_cache
    for key, (model, _) in _model_cache.items():
        try:
            del model
        except Exception:
            pass
    _model_cache.clear()
    import gc
    gc.collect()
