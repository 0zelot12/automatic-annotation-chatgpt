from dataclasses import dataclass


@dataclass
class Metrics:
    precision: float
    recall: float
    f1_score: float
    true_positives: int
    false_positives: int
    reference_count: int
