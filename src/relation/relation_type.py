from enum import Enum


class RelationType(Enum):
    ACTOR_PERFORMER = "actor performer"
    ACTOR_RECIPIENT = "actor recipient"
    SAME_GATEWAY = "same gateway"
    FURTHER_SPECIFICATION = "further specification"
    FLOW = "flow"
    USES = "uses"


def str_to_relation_type(string_value: str):
    for relation_type in RelationType:
        if relation_type.name == string_value or relation_type.value == string_value:
            return relation_type
    raise ValueError(f"RelationType has no member '{string_value}'")
