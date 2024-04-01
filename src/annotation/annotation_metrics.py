from dataclasses import dataclass

from annotation.metrics.entity_metrics import EntityMetrics
from annotation.metrics.metrics import Metrics
from annotation.metrics.relation_metrics import RelationMetrics


@dataclass
class AnnotationMetrics:
    overall_metrics: Metrics
    entity_metrics: EntityMetrics
    relation_metrics: RelationMetrics

    def to_json(self):
        return {
            "overall_metrics": self.overall_metrics.__dict__,
            "entity_metrics": self.entity_metrics.to_json(),
            "relation_metrics": self.relation_metrics.to_json(),
        }
