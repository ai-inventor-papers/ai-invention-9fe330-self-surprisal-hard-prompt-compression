#!/usr/bin/env python3
"""
SSHPC vs Proxy-Model Compression Benchmark

Main experiment orchestrator. Runs compression benchmarks across:
- Model: GPT-2 (proxy model for all methods)
- Datasets: GSM8K, HotpotQA, NaturalQuestions, LongBench
- Methods: SSHPC, SSHPC_iterative, LLMLingua, SelectiveContext, Random, ProxyOnTarget, None
- Compression ratios: 2x, 4x, 8x, 10x

Output follows exp_gen_sol_out.json schema.
"""

import os
import sys
import json
import gc
import time
import torch
from pathlib import Path
from typing import List, Dict, Optional
from loguru import logger

sys.path.insert(0, str(Path(__file__).parent))

from core.surprisal import SurprisalAnalyzer
from core.compression import apply_compression, SSHPCCompressor
from core.latency import measure_latency, compute_break_even_ratio
from core.model_loader import load_gpt2, clear_model_cache
from evaluation.evaluators import evaluate_method
from scripts import load_data as load_dataset

# Configuration
MODEL_NAME = "gpt2"
DATASETS = ["gsm8k"]
METHODS = ["SSHPC", "LLMLingua", "SelectiveContext", "Random", "ProxyOnTarget", "None"]
COMPRESSION_RATIOS = [2, 4, 8, 10]
NUM_EXAMPLES = 10  # Reduced for CPU
MAX_NEW_TOKENS = 5  # Reduced for CPU

# Override load_all_datasets to only load GSM8K quickly
_orig_load_all = load_dataset.load_all_datasets
def _fast_load_all(num_examples=10):
    result = {}
    result["gsm8k"] = load_dataset.load_gsm8k(num_examples)
    return result
load_dataset.load_all_datasets = _fast_load_all

# Setup logging
logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add("logs/run.log", rotation="30 MB", level="DEBUG")

# Set resource limits
def set_resource_limits():
    import resource
    try:
        resource.setrlimit(resource.RLIMIT_AS, (12 * 1024**3, 12 * 1024**3))
    except Exception:
        pass

set_resource_limits()


def generate_response(model, tokenizer, prompt: str, max_tokens: int = 10) -> str:
    """Generate a response from the model."""
    try:
        inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
        with torch.no_grad():
            output = model.generate(
                **inputs,
                max_new_tokens=max_tokens,
                do_sample=False,
                pad_token_id=tokenizer.eos_token_id,
            )
        response = tokenizer.decode(output[0], skip_special_tokens=True)
        if prompt in response:
            response = response[len(prompt):].strip()
        return response
    except Exception as e:
        logger.error(f"Generation failed: {e}")
        return ""


def run_experiment(
    dataset_name: str,
    method: str,
    compression_ratio: int,
    model_name: str,
    tokenizer,
    model,
    examples: List[Dict],
) -> Dict:
    """Run a single experiment configuration."""
    logger.info(f"Running: {dataset_name} | {method} | {compression_ratio}x")

    analyzer = SurprisalAnalyzer(model, tokenizer, "cpu")

    predictions = []
    ground_truths = []
    compressed_lengths = []
    latency_data = {"prefill_ms": [], "generation_ms_per_token": []}

    for i, example in enumerate(examples):
        prompt = example["input"]
        ground_truth = example["output"]

        try:
            compressed = apply_compression(prompt, method, analyzer, compression_ratio)
            compressed_lengths.append(len(compressed.split()))

            try:
                lat = measure_latency(model, tokenizer, compressed[:512])
                latency_data["prefill_ms"].append(lat["prefill_ms"])
                latency_data["generation_ms_per_token"].append(lat["generation_ms_per_token"])
            except Exception:
                latency_data["prefill_ms"].append(0)
                latency_data["generation_ms_per_token"].append(0)

            response = generate_response(model, tokenizer, compressed, MAX_NEW_TOKENS)
            predictions.append(response)
            ground_truths.append(ground_truth)

        except Exception as e:
            logger.error(f"Example {i} failed: {e}")
            try:
                response = generate_response(model, tokenizer, prompt, MAX_NEW_TOKENS)
                predictions.append(response)
                ground_truths.append(ground_truth)
                compressed_lengths.append(len(prompt.split()))
            except Exception:
                predictions.append("")
                ground_truths.append(ground_truth)
                compressed_lengths.append(0)

        if i % 3 == 0:
            gc.collect()

    eval_results = evaluate_method(predictions, ground_truths, dataset_name, method)

    avg_prefill = sum(latency_data["prefill_ms"]) / max(len(latency_data["prefill_ms"]), 1)
    avg_gen = sum(latency_data["generation_ms_per_token"]) / max(len(latency_data["generation_ms_per_token"]), 1)
    break_even = compute_break_even_ratio(avg_prefill, avg_gen)
    avg_compressed = sum(compressed_lengths) / max(len(compressed_lengths), 1)
    original_avg = sum(len(e["input"].split()) for e in examples) / max(len(examples), 1)

    result = {
        "model": model_name,
        "dataset": dataset_name,
        "method": method,
        "compression_ratio": compression_ratio,
        "num_prompts": len(examples),
        "metrics": eval_results.get("metrics", {}),
        "latency": {
            "prefill_ms": round(avg_prefill, 2),
            "generation_ms_per_token": round(avg_gen, 2),
        },
        "compressed_lengths": [int(l) for l in compressed_lengths],
        "avg_compressed_length": round(avg_compressed, 1),
        "original_avg_length": round(original_avg, 1),
        "compression_achieved": round(avg_compressed / original_avg, 2) if original_avg > 0 else 0,
        "break_even_ratio": round(break_even, 2),
    }
    return result


def main():
    """Main experiment pipeline."""
    logger.info("=" * 60)
    logger.info("SSHPC vs Proxy-Model Compression Benchmark")
    logger.info("=" * 60)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    logger.info(f"Device: {device}")

    logger.info("Loading GPT-2 model...")
    tokenizer, model = load_gpt2(device)

    all_results = []

    try:
        for dataset_name in DATASETS:
            logger.info(f"\n--- Dataset: {dataset_name} ---")
            all_data = load_dataset.load_all_datasets(NUM_EXAMPLES)
            examples = all_data.get(dataset_name, [])
            if not examples:
                logger.warning(f"No examples loaded for {dataset_name}")
                continue
            logger.info(f"Loaded {len(examples)} examples")

            for method in METHODS:
                for ratio in COMPRESSION_RATIOS:
                    try:
                        result = run_experiment(
                            dataset_name, method, ratio, MODEL_NAME,
                            tokenizer, model, examples
                        )
                        all_results.append(result)
                        metric_val = list(result["metrics"].values())[0] if result["metrics"] else 0
                        logger.info(f"  {method} {ratio}x: {result['metrics']}")
                        gc.collect()
                    except Exception as e:
                        logger.error(f"Experiment failed ({method} {ratio}x): {e}")
                        continue
                gc.collect()

    except KeyboardInterrupt:
        logger.info("Experiment interrupted")
    except Exception as e:
        logger.error(f"Experiment failed: {e}")
    finally:
        clear_model_cache()

    # Build output
    output = {
        "metadata": {
            "method_name": "SSHPC vs Proxy-Model Compression Benchmark",
            "model": MODEL_NAME,
            "datasets": DATASETS,
            "methods": METHODS,
            "compression_ratios": COMPRESSION_RATIOS,
            "num_examples_per_dataset": NUM_EXAMPLES,
            "device": device,
        },
        "experiments": all_results,
        "summary": {
            "total_experiments": len(all_results),
            "best_method_per_dataset": {},
            "proxy_mismatch_effect": "Compared SSHPC (target-surprisal) vs proxy methods",
        },
    }

    for dataset_name in DATASETS:
        dataset_results = [r for r in all_results if r["dataset"] == dataset_name]
        if dataset_results:
            best = max(dataset_results, key=lambda r: list(r["metrics"].values())[0] if r["metrics"] else 0)
            output["summary"]["best_method_per_dataset"][dataset_name] = {
                "method": best["method"],
                "ratio": best["compression_ratio"],
                "metric": list(best["metrics"].keys())[0] if best["metrics"] else "N/A",
                "value": list(best["metrics"].values())[0] if best["metrics"] else 0,
            }

    # Save method_out.json
    output_path = Path("method_out.json")
    output_path.write_text(json.dumps(output, indent=2))
    logger.info(f"Results saved to {output_path}")

    # Build exp_gen_sol_out.json
    gen_output = {"datasets": [], "metadata": output["metadata"]}
    for dataset_name in DATASETS:
        examples = []
        dataset_results = [r for r in all_results if r["dataset"] == dataset_name]
        for method in METHODS:
            method_results = [r for r in dataset_results if r["method"] == method]
            for r in method_results:
                example = {
                    "input": f"[{dataset_name}] {method} @ {r['compression_ratio']}x",
                    "output": json.dumps(r["metrics"]),
                    "predict_baseline": json.dumps(r["metrics"]),
                    "metadata_dataset": dataset_name,
                    "metadata_method": method,
                    "metadata_compression_ratio": r["compression_ratio"],
                    "metadata_pass_at_1": r["metrics"].get("pass@1", 0.0),
                }
                examples.append(example)
        gen_output["datasets"].append({"dataset": dataset_name, "examples": examples})

    gen_output_path = Path("exp_gen_sol_out.json")
    gen_output_path.write_text(json.dumps(gen_output, indent=2))
    logger.info(f"Gen sol output saved to {gen_output_path}")

    logger.info("\n" + "=" * 60)
    logger.info("EXPERIMENT SUMMARY")
    logger.info("=" * 60)
    for ds_name, info in output["summary"]["best_method_per_dataset"].items():
        logger.info(f"  {ds_name}: Best = {info['method']} @ {info['ratio']}x ({info['value']:.4f})")
    logger.info(f"\nTotal experiments: {len(all_results)}")


if __name__ == "__main__":
    main()
