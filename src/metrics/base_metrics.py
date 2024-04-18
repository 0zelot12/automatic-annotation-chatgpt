from dataclasses import dataclass


@dataclass
class BaseMetrics:
    precision: float
    recall: float
    f1_score: float
    true_positives: int
    false_positives: int
    reference_count: int

    def to_json(self):
        return {
            "precision": self.precision,
            "recall": self.recall,
            "f1_score": self.f1_score,
            "true_positives": self.true_positives,
            "false_positives": self.false_positives,
            "reference_count": self.reference_count,
        }
