import numpy as np

from dataclasses import dataclass, field

from entity.entity_type import EntityType, str_to_entity_type


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


def parse_entities(entity_strings: list[str], tokens: list[str]) -> list[Entity]:
    entities = []
    for entitiy_string in entity_strings:
        items = entitiy_string.split(",")

        entity_type = str_to_entity_type(items[0])
        start_index = int(items[1].replace("$", ""))
        end_index = int(items[2].replace("$", ""))

        parsed_entity = Entity(
            type=entity_type,
            start_index=start_index,
            end_index=end_index,
            tokens=tokens[start_index : end_index + 1],
        )

        entities.append(parsed_entity)

    return entities
