from enum import Enum


class EntityTag(Enum):

    B_ACTOR = "B-Actor"
    I_ACTOR = "I-Actor"
    B_ACTIVITY = "B-Activity"
    I_ACTIVITY = "I-Activity"
    B_ACTIVITY_DATA = "B-Activity Data"
    I_ACTIVITY_DATA = "I-Activity Data"
    B_FURTHER_SPECIFICATION = "B-Further Specification"
    I_FURTHER_SPECIFICATION = "I-Further Specification"
    B_AND_GATEWAY = "B-AND Gateway"
    I_AND_GATEWAY = "I-AND Gateway"
    B_XOR_GATEWAY = "B-XOR Gateway"
    I_XOR_GATEWAY = "I-XOR Gateway"
    B_CONDITION_SPECIFICATION = "B-Condition Specification"
    I_CONDITION_SPECIFICATION = "I-Condition Specification"
    NO_ENTITY = "O"


def str_to_entity(string_value: str) -> EntityTag:
    for entity in EntityTag:
        if entity.value == string_value:
            return entity
    return EntityTag.NO_ENTITY
