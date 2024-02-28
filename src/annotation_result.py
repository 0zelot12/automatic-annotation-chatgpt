from dataclasses import dataclass, field
from datetime import datetime
from annotation_metrics import AnnotationMetrics

from entity import Entity


@dataclass
class AnnotationResult:
    document_name: str
    metrics: AnnotationMetrics
    tokens: list[str] = field(default_factory=list)
    recognized_entities: list[Entity] = field(default_factory=list)
    present_entities: list[Entity] = field(default_factory=list)

    def __str__(self) -> str:
        tokens_str = ", ".join(self.tokens)
        recognized_entities_str = "\n".join(
            str(entity) for entity in self.recognized_entities
        )
        present_entities_str = "\n".join(
            str(entity) for entity in self.present_entities
        )

        return (
            f"Document Name: {self.document_name}\n"
            f"Precision: {self.metrics.precision}\n"
            f"Recall: {self.metrics.recall}\n"
            f"F1 Score: {self.metrics.f1_score}\n"
            f"Tokens: {tokens_str}\n"
            f"Recognized Entities:\n{recognized_entities_str}\n"
            f"Present Entities:\n{present_entities_str}\n"
        )

    def save_to_file(self, path: str) -> None:
        with open(
            f"{path}/{self.document_name}-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.txt",
            "w",
        ) as file:
            file.write(str(self))
