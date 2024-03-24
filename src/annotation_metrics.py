from dataclasses import dataclass


@dataclass
class Metrics:
    precision: float
    recall: float
    f1_score: float


@dataclass
class AnnotationMetrics:
    overall: Metrics
    actor: Metrics
    activity: Metrics
    activity_data: Metrics

    def to_json(self):
        return {
            "overall": self.overall.__dict__,
            "actor": self.actor.__dict__,
            "activity": self.activity.__dict__,
            "activity_data": self.activity_data.__dict__,
        }
