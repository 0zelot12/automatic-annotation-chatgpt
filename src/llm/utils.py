from relation.relation_type import RelationType
from relation.relation import Relation


def generate_model_relations(relations: list[Relation]) -> str:
    result = ""
    for relation in relations:
        source_length = (
            0 if len(relation.source.tokens) == 1 else len(relation.source.tokens) - 1
        )

        target_length = (
            0 if len(relation.target.tokens) == 1 else len(relation.target.tokens) - 1
        )

        result += f"${relation.source.start_index},${relation.source.start_index + source_length},{relation.type.name},${relation.target.start_index}${relation.target.start_index + target_length}\n"

    return result
