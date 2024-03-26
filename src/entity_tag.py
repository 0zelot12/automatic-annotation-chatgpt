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
    NO_ENTITY = "O"


def str_to_entity(string_value: str) -> EntityTag:
    for entity in EntityTag:
        if entity.value == string_value:
            return entity
    return EntityTag.NO_ENTITY
