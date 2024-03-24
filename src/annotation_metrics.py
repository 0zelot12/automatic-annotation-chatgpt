from dataclasses import dataclass


@dataclass
class AnnotationMetrics:
    precision: float
    recall: float
    f1_score: float

    actor_precision: float
    actor_recall: float
    actor_f1_score: float

    activity_precision: float
    activity_recall: float
    activity_f1_score: float

    activity_data_precision: float
    activity_data_recall: float
    activity_data_f1_score: float

    def to_json(self):
        return {
            "precision": self.precision,
            "recall": self.recall,
            "f1_score": self.f1_score,
            "actor_precision": self.actor_precision,
            "actor_recall": self.actor_recall,
            "actor_f1_score": self.actor_f1_score,
            "activity_precision": self.activity_precision,
            "activity_recall": self.activity_recall,
            "activity_f1_score": self.activity_f1_score,
            "activity_data_precision": self.activity_data_precision,
            "activity_data_recall": self.activity_data_recall,
            "activity_data_f1_score": self.activity_data_f1_score,
        }
