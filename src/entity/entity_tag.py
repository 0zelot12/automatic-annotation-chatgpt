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
    B_AND_GATEWAY = ""
    I_AND_GATEWAY = ""
    B_XOR_GATEWAY = ""
    I_XOR_GATEWAY = ""
    B_CONDITION_SPECIFICATION = ""
    I_CONDITION_SPECIFICATION = ""
    NO_ENTITY = "O"


def str_to_entity(string_value: str) -> EntityTag:
    for entity in EntityTag:
        if entity.value == string_value:
            return entity
    return EntityTag.NO_ENTITY
