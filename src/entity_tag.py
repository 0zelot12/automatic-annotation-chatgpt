from enum import Enum


class EntityTag(Enum):
    """
    Enum representing entities in the PET dataset.

    The PET dataset consists of various entities, each serving a specific role in the data. This Enum class defines
    the possible entities with their corresponding labels.

    Enum Values:
        - B_ACTOR: Represents the beginning of an entity labeled as "Actor" in the PET dataset.
        - I_ACTOR: Represents an intermediate part of an entity labeled as "Actor" in the PET dataset.
        - B_ACTIVITY: Represents the beginning of an entity labeled as "Activity" in the PET dataset.
        - I_ACTIVITY: Represents an intermediate part of an entity labeled as "Activity" in the PET dataset.
        - B_ACTIVITY_DATA: Represents the beginning of an entity labeled as "Activity Data" in the PET dataset.
        - I_ACTIVITY_DATA: Represents an intermediate part of an entity labeled as "Activity Data" in the PET dataset.
        - B_FURTHER_SPECIFICATION: Represents the beginning of an entity labeled as "Further Specification" in the PET dataset.
        - I_FURTHER_SPECIFICATION: Represents an intermediate part of an entity labeled as "Further Specification" in the PET dataset.
        - NO_ENTITY: Represents the absence of a specific entity, labeled as "O" in the PET dataset.

    Example:
        ```
        # Usage of Entity Enum
        entity_type = Entity.B_ACTOR
        print(entity_type.value)  # Output: "B-Actor"
        ```

    Note:
        This Enum class provides a convenient and readable way to work with entity labels in the PET dataset.
    """

    B_ACTOR = "B-Actor"
    I_ACTOR = "I-Actor"
    B_ACTIVITY = "B-Activity"
    I_ACTIVITY = "I-Activity"
    B_ACTIVITY_DATA = "B-Activity Data"
    I_ACTIVITY_DATA = "I-Activity Data"
    B_FURTHER_SPECIFICATION = "B-Further Specification"
    I_FURTHER_SPECIFICATION = "I-Further Specification"
    NO_ENTITY = "O"


def isActor(entity: EntityTag):
    return entity == EntityTag.B_ACTOR or entity == EntityTag.I_ACTOR


def isActivity(entity: EntityTag):
    return entity == EntityTag.B_ACTIVITY or entity == EntityTag.I_ACTIVITY


def isActivityData(entity: EntityTag):
    return entity == EntityTag.B_ACTIVITY_DATA or entity == EntityTag.I_ACTIVITY_DATA


def str_to_entity(string_value: str) -> EntityTag:
    """
    Converts a string representation of an entity label to the corresponding Entity Enum value.

    Args:
        string_value (str): The string representation of the entity label.

    Returns:
        Entity: The corresponding Entity Enum value.
    """
    for entity in EntityTag:
        if entity.value == string_value:
            return entity
    return EntityTag.NO_ENTITY
