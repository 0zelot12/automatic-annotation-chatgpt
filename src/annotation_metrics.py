from dataclasses import dataclass


@dataclass
class AnnotationMetrics:
    precision: float
    recall: float
    f1_score: float

    def to_json(self):
        return {
            "precision": self.precision,
            "recall": self.recall,
            "f1_score": self.f1_score,
        }
