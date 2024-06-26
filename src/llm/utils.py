from relation.relation_type import RelationType
from relation.relation import Relation

from entity.entity import Entity


def to_model_tokens(tokens: list[str]):
    result = ""
    for token, index in zip(tokens, range(0, len(tokens))):
        result += f"{token}${index}\n"
    return result


def generate_model_relations(relations: list[Relation]) -> str:
    result = ""
    for relation in relations:
        source_length = (
            0 if len(relation.source.tokens) == 1 else len(relation.source.tokens) - 1
        )

        target_length = (
            0 if len(relation.target.tokens) == 1 else len(relation.target.tokens) - 1
        )

        result += f"{relation.source.type.name},${relation.source.start_index},${relation.source.start_index + source_length},{relation.type.name},{relation.target.type.name},${relation.target.start_index},${relation.target.start_index + target_length}\n"

    return result


def generate_model_entities(entities: list[Entity]) -> str:
    result = ""
    for entity in entities:
        entity_length = 0 if len(entity.tokens) == 1 else len(entity.tokens) - 1
        result += f"{entity.type.name},${entity.start_index},${entity.start_index + entity_length}\n"

    return result
