from dataclasses import dataclass


@dataclass
class Metrics:
    precision: float
    recall: float
    f1_score: float
    true_positives: int
    false_positives: int
    reference_count: int


@dataclass
class AnnotationMetrics:
    overall: Metrics
    actor: Metrics
    activity: Metrics
    activity_data: Metrics
    further_specification: Metrics
    and_gateway: Metrics
    xor_gateway: Metrics
    condition_specification: Metrics

    def to_json(self):
        return {
            "overall": self.overall.__dict__,
            "actor": self.actor.__dict__,
            "activity": self.activity.__dict__,
            "activity_data": self.activity_data.__dict__,
            "further_specification": self.further_specification.__dict__,
            "and_gateway": self.and_gateway.__dict__,
            "xor_gateway": self.xor_gateway.__dict__,
            "condition_specification": self.condition_specification.__dict__,
        }
