"""
Dataset loading module. Loads GSM8K, HotpotQA, NaturalQuestions, LongBench from HuggingFace.
"""
from datasets import load_dataset
from typing import List, Dict
from loguru import logger


def load_gsm8k(num_examples: int = 500) -> List[Dict]:
    logger.info(f"Loading GSM8K ({num_examples} examples)")
    try:
        ds = load_dataset("openai/gsm8k", "main", split=f"train[:{num_examples}]")
        return [{"input": item["question"], "output": item["answer"], "dataset": "gsm8k"} for item in ds]
    except Exception as e:
        logger.error(f"Failed to load GSM8K: {e}")
        return []


def load_hotpotqa(num_examples: int = 500) -> List[Dict]:
    logger.info(f"Loading HotpotQA ({num_examples} examples)")
    try:
        ds = load_dataset("hotpotqa/hotpot_qa", "distractor", split=f"train[:{num_examples}]")
        examples = []
        for item in ds:
            context = " ".join(item.get("context", []))
            question = item.get("question", "")
            answer = item.get("answer", "")
            examples.append({"input": f"Context: {context}\n\nQuestion: {question}", "output": answer, "dataset": "hotpotqa"})
        return examples
    except Exception as e:
        logger.error(f"Failed to load HotpotQA: {e}")
        return []


def load_naturalquestions(num_examples: int = 500) -> List[Dict]:
    logger.info(f"Loading NaturalQuestions ({num_examples} examples)")
    try:
        ds = load_dataset("google-research-datasets/natural_questions", "default", split=f"train[:{num_examples}]")
        examples = []
        for item in ds:
            question = item.get("question_text", "")
            answer = item.get("answer", "")
            if not question:
                continue
            examples.append({"input": question, "output": answer, "dataset": "naturalquestions"})
        return examples
    except Exception as e:
        logger.error(f"Failed to load NaturalQuestions: {e}")
        return []


def load_longbench_qa(num_examples: int = 500) -> List[Dict]:
    logger.info(f"Loading LongBench QA ({num_examples} examples)")
    try:
        ds = load_dataset("zai-org/longbench", "default", split=f"train[:{num_examples}]")
        examples = []
        for item in ds:
            question = item.get("input", "")
            answer = item.get("targets", "")
            if not question:
                continue
            examples.append({"input": question, "output": str(answer) if answer else "", "dataset": "longbench"})
        return examples
    except Exception as e:
        logger.error(f"Failed to load LongBench: {e}")
        return []


def load_all_datasets(num_examples: int = 50) -> Dict[str, List[Dict]]:
    return {
        "gsm8k": load_gsm8k(num_examples),
        "hotpotqa": load_hotpotqa(num_examples),
        "naturalquestions": load_naturalquestions(num_examples),
        "longbench": load_longbench_qa(num_examples),
    }

# Load quickly available datasets
def load_gsm8k_quick(num_examples: int = 50) -> List[Dict]:
    """Load GSM8K which is fast to load."""
    return load_gsm8k(num_examples)
