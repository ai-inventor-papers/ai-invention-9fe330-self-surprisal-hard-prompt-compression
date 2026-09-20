"""
Task evaluators for GSM8K, HotpotQA, LongBench, NaturalQuestions.
"""
import re
from typing import Dict, List
from loguru import logger


def compute_em_f1(pred: str, ground_truth: str) -> Dict[str, float]:
    pred = pred.strip().lower()
    gt = ground_truth.strip().lower()
    if pred == gt:
        return {"em": 1.0, "f1": 1.0}
    pred_tokens = pred.split()
    gt_tokens = gt.split()
    if not pred_tokens or not gt_tokens:
        return {"em": 0.0, "f1": 0.0}
    pred_set = {}
    gt_set = {}
    for t in pred_tokens:
        pred_set[t] = pred_set.get(t, 0) + 1
    for t in gt_tokens:
        gt_set[t] = gt_set.get(t, 0) + 1
    common = set(pred_set.keys()) & set(gt_set.keys())
    if not common:
        return {"em": 0.0, "f1": 0.0}
    num_same = sum(min(pred_set[t], gt_set[t]) for t in common)
    precision = num_same / len(pred_tokens) if pred_tokens else 0
    recall = num_same / len(gt_tokens) if gt_tokens else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    return {"em": 1.0 if pred == gt else 0.0, "f1": f1}


def extract_number(text: str):
    numbers = re.findall(r'-?\d+\.?\d*', text)
    if numbers:
        try:
            return float(numbers[-1])
        except ValueError:
            return None
    return None


def eval_gsm8k(prediction: str, ground_truth: str) -> Dict[str, float]:
    pred_num = extract_number(prediction)
    gt_num = extract_number(ground_truth)
    if pred_num is not None and gt_num is not None:
        if abs(pred_num - gt_num) < 0.01 * abs(gt_num) or abs(pred_num - gt_num) < 0.01:
            return {"pass@1": 1.0, "exact_match": 1.0}
    em = 1.0 if prediction.strip().lower() == ground_truth.strip().lower() else 0.0
    return {"pass@1": em, "exact_match": em}


def eval_hotpotqa(prediction: str, ground_truth: str) -> Dict[str, float]:
    return compute_em_f1(prediction, ground_truth)


def eval_longbench(prediction: str, ground_truth: str) -> Dict[str, float]:
    return compute_em_f1(prediction, ground_truth)


def eval_naturalquestions(prediction: str, ground_truth: str) -> Dict[str, float]:
    return compute_em_f1(prediction, ground_truth)


def evaluate_method(
    predictions: List[str],
    ground_truths: List[str],
    task: str,
    method_name: str,
) -> Dict:
    results = {
        "method": method_name,
        "task": task,
        "num_samples": len(predictions),
        "metrics": {},
    }
    if task == "gsm8k":
        pass_at_1 = 0.0
        for pred, gt in zip(predictions, ground_truths):
            result = eval_gsm8k(pred, gt)
            pass_at_1 += result["pass@1"]
        pass_at_1 /= len(predictions) if predictions else 1
        results["metrics"] = {"pass@1": round(pass_at_1, 4)}
    elif task == "hotpotqa":
        em_sum = 0.0
        f1_sum = 0.0
        for pred, gt in zip(predictions, ground_truths):
            result = eval_hotpotqa(pred, gt)
            em_sum += result["em"]
            f1_sum += result["f1"]
        results["metrics"] = {
            "em": round(em_sum / len(predictions), 4) if predictions else 0,
            "f1": round(f1_sum / len(predictions), 4) if predictions else 0,
        }
    elif task == "longbench":
        em_sum = 0.0
        for pred, gt in zip(predictions, ground_truths):
            result = eval_longbench(pred, gt)
            em_sum += result["em"]
        results["metrics"] = {"em": round(em_sum / len(predictions), 4) if predictions else 0}
    elif task == "naturalquestions":
        em_sum = 0.0
        f1_sum = 0.0
        for pred, gt in zip(predictions, ground_truths):
            result = eval_naturalquestions(pred, gt)
            em_sum += result["em"]
            f1_sum += result["f1"]
        results["metrics"] = {
            "em@1": round(em_sum / len(predictions), 4) if predictions else 0,
            "f1@1": round(f1_sum / len(predictions), 4) if predictions else 0,
        }
    return results
