from enum import Enum


class EntityType(Enum):
    ACTOR = "ACTOR"
    ACTIVITY = "ACTIVITY"
    ACTIVITY_DATA = "ACTIVITY_DATA"
    FURTHER_SPECIFICATION = "FURTHER_SPECIFICATION"
    AND_GATEWAY = "AND_GATEWAY"
    XOR_GATEWAY = "XOR_GATEWAY"
    CONDITION_SPECIFICATION = "CONDITION_SPECIFICATION"


def str_to_entity_type(string_value: str) -> EntityType:
    for entity in EntityType:
        if entity.value == string_value:
            return entity
    raise ValueError(f"EntityType has no member '{string_value}'")
