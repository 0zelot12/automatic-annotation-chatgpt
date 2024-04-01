from dataclasses import dataclass

from metrics.base_metrics import BaseMetrics


@dataclass
class RelationMetrics:
    overall: BaseMetrics
    actor_performer: BaseMetrics
    actor_recipient: BaseMetrics
    same_gateway: BaseMetrics
    further_specification: BaseMetrics
    flow: BaseMetrics
    uses: BaseMetrics

    def to_json(self):
        return {
            "overall": self.overall.__dict__,
            "actor_performer": self.actor_performer.__dict__,
            "actor_recipient": self.actor_recipient.__dict__,
            "same_gateway": self.same_gateway.__dict__,
            "further_specification": self.further_specification.__dict__,
            "flow": self.flow.__dict__,
            "uses": self.uses.__dict__,
        }
