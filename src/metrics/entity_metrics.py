from dataclasses import dataclass

from metrics.base_metrics import BaseMetrics


@dataclass
class EntityMetrics:
    overall: BaseMetrics
    actor: BaseMetrics
    activity: BaseMetrics
    activity_data: BaseMetrics
    further_specification: BaseMetrics
    and_gateway: BaseMetrics
    xor_gateway: BaseMetrics
    condition_specification: BaseMetrics

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
