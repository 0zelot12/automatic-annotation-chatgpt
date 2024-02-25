from dataclasses import dataclass, field

from entity_type import EntityType


@dataclass
class Entity:
    type: EntityType
    tokens: list[str] = field(default_factory=list)
    start_index: int
