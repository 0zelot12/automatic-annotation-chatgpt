from dataclasses import dataclass, field

from entity import Entity
from relation_type import RelationType


@dataclass
class Relation:
    type: RelationType
    source: Entity
    target: Entity


def str_to_type(string_value: str) -> RelationType:
    for type in RelationType:
        if type.value == string_value:
            return type
    raise ValueError()
