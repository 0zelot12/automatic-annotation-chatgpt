from dataclasses import dataclass, field

from entity import Entity


@dataclass
class AnnotationResult:
    document_name: str
    recognized_entities: list[Entity] = field(default_factory=list)
    present_entities: list[Entity] = field(default_factory=list)

    def get_precision(self) -> float:
        """
        Precision is the number of NEs a system correctly detects divided by the total number of NEs identified by the system.
        """

        # TODO: Implement

        return 0.0

    def get_recall(self) -> float:
        """
        Recall is the number of NEs a system correctly detected divided by the total number of NEs contained in the input text.
        """

        # TODO: Implement

        return 0.0

    def get_f1_score(self) -> float:
        precision = self.get_precision()
        recall = self.get_recall()
        return round(2 * precision * recall / (precision + recall), 2)
