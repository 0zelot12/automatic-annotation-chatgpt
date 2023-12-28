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
    response_time: int = 0
    recognized_o: int = 0
    expected_o: int = 0
    expected_actor: int = 0
    recognized_actor: int = 0
    expected_activity: int = 0
    recognized_activity: int = 0
    expected_activity_data: int = 0
    recognized_activity_data: int = 0
    incorrect_entities: int = 0

    # TODO: Output als Text bereitstellen
