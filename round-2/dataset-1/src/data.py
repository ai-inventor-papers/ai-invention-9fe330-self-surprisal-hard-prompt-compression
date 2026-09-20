#!/usr/bin/env python3
"""Load standardized datasets from data_out/ and produce full_data_out.json in exp_sel_data_out schema."""

from loguru import logger
import sys
import json
from pathlib import Path
from collections import defaultdict

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add("logs/run.log", rotation="30 MB", level="DEBUG")

DATA_DIR = Path("data_out")
OUTPUT_FILE = Path("full_data_out.json")


def load_all_examples():
    """Load all examples from split files in data_out/."""
    all_examples = []
    for part_file in sorted(DATA_DIR.glob("data_out_*.json")):
        with open(part_file) as f:
            data = json.load(f)
        all_examples.extend(data)
    return all_examples


def group_by_dataset(examples):
    """Group examples by dataset name."""
    groups = defaultdict(list)
    for i, ex in enumerate(examples):
        dataset_name = ex.get("dataset", "unknown")
        groups[dataset_name].append({
            "input": ex.get("prompt", ""),
            "output": ex.get("answer", ""),
            "metadata_task_type": ex.get("task_type", "unknown"),
            "metadata_split": ex.get("split", "unknown"),
            "metadata_row_index": i,
        })
    return groups


BEST_DATASETS = [
    "gsm8k",
    "hotpotqa",
    "musique",
    "squad",
    "ropes",
    "arxiv",
    "govreport",
    "narrativeqa",
    "trivia_qa",
]


def build_output(groups):
    """Build the exp_sel_data_out schema structure with only best 9 datasets."""
    datasets = []
    for dataset_name, examples in sorted(groups.items()):
        if dataset_name not in BEST_DATASETS:
            continue
        datasets.append({
            "dataset": dataset_name,
            "examples": examples,
        })
    return {
        "metadata": {
            "description": "Prompt Compression Benchmark Datasets",
            "total_examples": sum(len(d["examples"]) for d in datasets),
            "num_datasets": len(datasets),
            "task_types": list(set(
                ex.get("metadata_task_type", "")
                for d in datasets
                for ex in d["examples"]
            )),
        },
        "datasets": datasets,
    }


@logger.catch(reraise=True)
def main():
    logger.info(f"Loading examples from {DATA_DIR}...")
    examples = load_all_examples()
    logger.info(f"Loaded {len(examples)} total examples")

    logger.info("Grouping by dataset...")
    groups = group_by_dataset(examples)
    logger.info(f"Found {len(groups)} datasets")

    for name, exs in sorted(groups.items()):
        logger.info(f"  {name}: {len(exs)} examples")

    logger.info("Building output...")
    output = build_output(groups)

    logger.info(f"Saving to {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, "w") as f:
        json.dump(output, f)

    size = OUTPUT_FILE.stat().st_size
    logger.info(f"Saved {size / 1e6:.1f}MB")

    # Verify structure
    total = sum(len(d["examples"]) for d in output["datasets"])
    logger.info(f"Verification: {output['metadata']['num_datasets']} datasets, {total} total examples")


if __name__ == "__main__":
    main()
