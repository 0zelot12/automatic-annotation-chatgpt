import json

from dataclasses import dataclass, field
from datetime import datetime

from annotation.entity_metrics import EntityMetrics
from entity.entity import Entity
from relation.relation import Relation

# TODO: Write a test to check if AnnotationResult can be saved to a file


@dataclass
class AnnotationResult:
    document_name: str
    document_length: int
    temperature: float
    prompt_type: str
    metrics: EntityMetrics
    api_response: list[str] = field(default_factory=list)
    examples_documents: list[str] = field(default_factory=list)
    tokens: list[str] = field(default_factory=list)
    recognized_entities: list[Entity] = field(default_factory=list)
    present_entities: list[Entity] = field(default_factory=list)
    present_relations: list[Relation] = field(default_factory=list)
    recognized_relations: list[Relation] = field(default_factory=list)

    def to_json(self):
        return {
            "document_name": self.document_name,
            "metrics": self.metrics.to_json(),
            "document_length": self.document_length,
            "prompt_type": self.prompt_type,
            "examples_documents": self.examples_documents,
            "tokens": [
                str(token) for token in self.tokens
            ],  # TODO: Check why this is needed in Windows
            "recognized_entities": [
                entity.to_json() for entity in self.recognized_entities
            ],
            "present_entities": [entity.to_json() for entity in self.present_entities],
            "present_relations": [
                relation.to_json() for relation in self.present_relations
            ],
            "recognized_relations": [
                relation.to_json() for relation in self.recognized_relations
            ],
            "api_response": self.api_response,
        }

    # Refactor to a generic method that saves JSON objects
    def save_to_file(self, path: str) -> None:
        with open(
            f"{path}/{self.document_name}-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.json",
            "w",
        ) as file:
            file.write(json.dumps(self.to_json()))
