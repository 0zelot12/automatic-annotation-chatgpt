from dataclasses import dataclass, field

from entity.entity_type import EntityType


@dataclass
class Entity:
    type: EntityType
    start_index: int
    tokens: list[str] = field(default_factory=list)

    def __hash__(self):
        return hash((self.type, self.start_index, tuple(self.tokens)))

    def __str__(self) -> str:
        length = 0 if len(self.tokens) == 1 else len(self.tokens) - 1
        return f"{self.type.name},${self.start_index},${self.start_index + length}"

    def to_json(self):
        return {
            "type": self.type.name,
            "start_index": self.start_index,
            "tokens": self.tokens,
        }
