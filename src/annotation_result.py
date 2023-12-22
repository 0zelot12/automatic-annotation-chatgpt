from dataclasses import dataclass


@dataclass
class AnnotationResult:
    input_length: int = 0
    recognized_o: int = 0
    expected_o: int = 0
    expected_actor: int = 0
    recognized_actor: int = 0
    expected_activity: int = 0
    recognized_activity: int = 0
    expected_activity_data: int = 0
    recognized_activity_data: int = 0
