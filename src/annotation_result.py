from dataclasses import dataclass


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
