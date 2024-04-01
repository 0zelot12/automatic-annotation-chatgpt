from dataclasses import dataclass

from annotation.metrics.metrics import Metrics


@dataclass
class RelationMetrics:
    overall: Metrics
    actor_performer: Metrics
    actor_recipient: Metrics
    same_gateway: Metrics
    further_specification: Metrics
    flow: Metrics
    uses: Metrics

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
