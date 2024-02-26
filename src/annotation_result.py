from dataclasses import dataclass, field

from entity import Entity


@dataclass
class AnnotationResult:
    document_name: str
    precision: float
    recall: float
    f1_score: float
    tokens: list[str] = field(default_factory=list)
    recognized_entities: list[Entity] = field(default_factory=list)
    present_entities: list[Entity] = field(default_factory=list)
