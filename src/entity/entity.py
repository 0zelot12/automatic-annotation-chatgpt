import numpy as np

from dataclasses import dataclass, field

from entity.entity_type import EntityType

# TODO: Tokens are not needed and can be replaced by end_index


@dataclass
class Entity:
    type: EntityType
    start_index: int
    tokens: list[str] = field(default_factory=list)

    def get_index_range(self):
        return (
            [self.start_index]
            if len(self.tokens) == 1
            else list(np.arange(self.start_index, self.start_index + len(self.tokens)))
        )

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
