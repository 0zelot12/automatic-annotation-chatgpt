from dataclasses import dataclass, field

from entity import Entity
from relation_type import RelationType


@dataclass
class Relation:
    type: RelationType
    source: Entity
    target: Entity

    def to_json(self):
        return {
            "type": self.type.value,
            "source": None if not self.source else self.source.to_json(),
            "target": None if not self.target else self.target.to_json(),
        }


def str_to_type(string_value: str) -> RelationType:
    for type in RelationType:
        if type.value == string_value:
            return type
    raise ValueError()
