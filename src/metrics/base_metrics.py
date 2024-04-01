from dataclasses import dataclass


@dataclass
class BaseMetrics:
    precision: float
    recall: float
    f1_score: float
    true_positives: int
    false_positives: int
    reference_count: int
