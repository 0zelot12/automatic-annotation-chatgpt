from enum import StrEnum


class Entity(StrEnum):
    """Enum representing the entities present in the PET dataset."""

    ACTOR = "Actor"
    ACTIVITY = "Activity"
    ACTIVITY_DATA = "Activity Data"
    FURTHER_SPECIFICATION = "Further Specification"
    NO_ENTITY = "O"


def str_to_entity(string_value):
    for entity in Entity:
        if entity.value == string_value:
            return entity
    raise ValueError
