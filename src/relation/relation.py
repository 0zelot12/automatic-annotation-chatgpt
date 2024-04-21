from dataclasses import dataclass

from entity.entity import Entity

from entity.entity_type import str_to_entity_type
from relation.relation_type import RelationType, str_to_relation_type


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

    def __str__(self) -> str:
        return f"{self.source.type.name},${self.source.start_index},${self.source.end_index},{self.type.name},{self.target.type.name},${self.target.start_index},${self.target.end_index}\n"


def parse_relations(relation_strings: list[str], tokens: list[str]) -> list[Relation]:
    relations = []
    for relation_string in relation_strings:
        items = relation_string.split(",")

        source_entity_type = str_to_entity_type(items[0])
        source_start_index = int(items[1].replace("$", ""))
        source_end_index = int(items[2].replace("$", ""))

        relation_type = str_to_relation_type(items[3])

        target_entity_type = str_to_entity_type(items[4])
        target_start_index = int(items[5].replace("$", ""))
        target_end_index = int(items[6].replace("$", ""))

        target = Entity(
            type=target_entity_type,
            start_index=target_start_index,
            end_index=target_end_index,
            tokens=tokens[target_start_index:target_end_index],
        )

        source = Entity(
            type=source_entity_type,
            start_index=source_start_index,
            end_index=source.end_index,
            tokens=tokens[source_start_index:source_end_index],
        )

        relations.append(Relation(source=source, target=target, type=relation_type))

    return relations
