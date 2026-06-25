import math
from typing import List, Dict

def precision_at_k(actual: List[str], predicted: List[str], k: int) -> float:
    """Calculate Precision@k."""
    if k == 0:
        return 0.0
    predicted_k = predicted[:k]
    relevant_retrieved = len(set(actual) & set(predicted_k))
    return relevant_retrieved / k

def recall_at_k(actual: List[str], predicted: List[str], k: int) -> float:
    """Calculate Recall@k."""
    if not actual:
        return 0.0
    predicted_k = predicted[:k]
    relevant_retrieved = len(set(actual) & set(predicted_k))
    return relevant_retrieved / len(actual)

def dcg_at_k(relevances: List[float], k: int) -> float:
    """Calculate Discounted Cumulative Gain at k."""
    dcg = 0.0
    for i, rel in enumerate(relevances[:k]):
        dcg += rel / math.log2(i + 2)  # i+2 because index is 0-based and formula uses log2(rank+1) where rank is 1-based
    return dcg

def ndcg_at_k(actual_relevances: List[float], predicted_relevances: List[float], k: int) -> float:
    """Calculate Normalized Discounted Cumulative Gain at k.
    actual_relevances should be sorted in ideal order.
    predicted_relevances should be the relevances of the items returned by the system in order.
    """
    ideal_dcg = dcg_at_k(sorted(actual_relevances, reverse=True), k)
    if ideal_dcg == 0.0:
        return 0.0
    actual_dcg = dcg_at_k(predicted_relevances, k)
    return actual_dcg / ideal_dcg

def ranking_quality(actual: List[str], predicted: List[str], k: int) -> Dict[str, float]:
    """Calculate an overall quality metrics dictionary."""
    return {
        "precision_at_k": precision_at_k(actual, predicted, k),
        "recall_at_k": recall_at_k(actual, predicted, k)
    }
