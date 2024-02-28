from dataclasses import dataclass


@dataclass
class AnnotationMetrics:
    precision: float
    recall: float
    f1_score: float
