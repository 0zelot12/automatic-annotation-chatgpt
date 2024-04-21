import numpy as np

from dataclasses import dataclass, field

from entity.entity_type import EntityType


@dataclass
class Entity:
    type: EntityType
    start_index: int
    end_index: int
    tokens: list[str] = field(default_factory=list)

    def get_index_range(self):
        return (
            [self.start_index]
            if len(self.tokens) == 1
            else list(np.arange(self.start_index, self.end_index))
        )

    def __hash__(self):
        return hash((self.type, self.start_index, self.end_index))

    def __str__(self) -> str:
        return f"{self.type.name},${self.start_index},${self.end_index}"

    def to_json(self):
        return {
            "type": self.type.name,
            "start_index": self.start_index,
            "start_index": self.end_index,
            "tokens": self.tokens,
        }
