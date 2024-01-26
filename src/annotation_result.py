from dataclasses import dataclass, field
from entity import Entity


@dataclass
class AnnotationResult:
    """
    Data class to store statistics for an annotated document.

    This class is designed to hold statistical information related to the annotation of a document. It provides
    attributes for various metrics, offering insights into the annotation process.

    Note:
    This data class simplifies the organization and access of annotation statistics, making it easy to work with
    and analyze the results of document annotation processes.
    """

    document_name: str
    input_length: int = 0
    recognized_o: int = 0
    expected_o: int = 0
    expected_actor: int = 0
    recognized_actor: int = 0
    expected_activity: int = 0
    recognized_activity: int = 0
    expected_activity_data: int = 0
    recognized_activity_data: int = 0
    incorrect_entities: int = 0
    total_number_of_entities: int = 0
    annotated_tokens: list[str] = field(default_factory=list)
    reference_annotated_tokens: list[str] = field(default_factory=list)
    # TODO: Implement
    ner_tags: list[Entity] = field(default_factory=list)
    reference_ner_tags: list[Entity] = field(default_factory=list)

    def get_precision(self) -> float:
        """
        Precision is the number of NEs a system correctly detects divided by the total number of NEs identified by the system.
        """

        entities_detected_correctly = sum(
            [
                self.recognized_actor,
                self.recognized_activity,
                self.recognized_activity_data,
            ]
        )

        entities_detected_total = sum(
            [
                self.recognized_actor,
                self.recognized_activity,
                self.recognized_activity_data,
                self.incorrect_entities,
            ]
        )

        return round(entities_detected_correctly / entities_detected_total, 2)

    def get_recall(self) -> float:
        """
        Recall is the number of NEs a system correctly detected divided by the total number of NEs contained in the input text.
        """

        entities_detected_correctly = sum(
            [
                self.recognized_actor,
                self.recognized_activity,
                self.recognized_activity_data,
            ]
        )

        return round(entities_detected_correctly / self.total_number_of_entities, 2)

    def get_f1_score(self) -> float:
        precision = self.get_precision()
        recall = self.get_recall()
        return round(2 * precision * recall / (precision + recall), 2)
