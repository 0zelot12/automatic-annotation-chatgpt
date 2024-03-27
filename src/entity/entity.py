from dataclasses import dataclass, field

from entity.entity_type import EntityType


@dataclass
class Entity:
    type: EntityType
    start_index: int
    tokens: list[str] = field(default_factory=list)

    def to_json(self):
        return {
            "type": self.type.name,
            "start_index": self.start_index,
            "tokens": self.tokens,
        }
