from enum import Enum


class Entity(Enum):
    """
    Enum representing entities in the PET dataset.

    The PET dataset consists of various entities, each serving a specific role in the data. This Enum class defines
    the possible entities with their corresponding labels.

    Enum Values:
        - ACTOR: Represents an entity labeled as "Actor" in the PET dataset.
        - ACTIVITY: Represents an entity labeled as "Activity" in the PET dataset.
        - ACTIVITY_DATA: Represents an entity labeled as "Activity Data" in the PET dataset.
        - FURTHER_SPECIFICATION: Represents an entity labeled as "Further Specification" in the PET dataset.
        - NO_ENTITY: Represents the absence of a specific entity, labeled as "O" in the PET dataset.

    Example:
        ```
        # Usage of Entity Enum
        entity_type = Entity.ACTOR
        print(entity_type.value)  # Output: "Actor"
        ```

    Note:
        This Enum class provides a convenient and readable way to work with entity labels in the PET dataset.
    """

    ACTOR = "Actor"
    ACTIVITY = "Activity"
    ACTIVITY_DATA = "Activity Data"
    FURTHER_SPECIFICATION = "Further Specification"
    NO_ENTITY = "O"


def str_to_entity(string_value: str) -> Entity:
    for entity in Entity:
        if entity.value == string_value:
            return entity
    raise ValueError
