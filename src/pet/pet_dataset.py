import platform

import pandas as pd

from typing import Tuple

from entity.entity import Entity
from entity.entity_type import EntityType
from entity.entity_tag import EntityTag, str_to_entity_tag

from pet.pet_document import PetDocument

from relation.relation import Relation
from relation.relation_type import str_to_relation_type


def get_tags(entityType: EntityType) -> Tuple[EntityTag, EntityTag]:
    if entityType == EntityType.ACTOR:
        return (EntityTag.B_ACTOR, EntityTag.I_ACTOR)
    elif entityType == EntityType.ACTIVITY:
        return (EntityTag.B_ACTIVITY, EntityTag.I_ACTIVITY)
    elif entityType == EntityType.ACTIVITY_DATA:
        return (EntityTag.B_ACTIVITY_DATA, EntityTag.I_ACTIVITY_DATA)
    elif entityType == EntityType.AND_GATEWAY:
        return (EntityTag.B_AND_GATEWAY, EntityTag.I_AND_GATEWAY)
    elif entityType == EntityType.XOR_GATEWAY:
        return (EntityTag.B_XOR_GATEWAY, EntityTag.I_XOR_GATEWAY)
    elif entityType == EntityType.CONDITION_SPECIFICATION:
        return (
            EntityTag.B_CONDITION_SPECIFICATION,
            EntityTag.I_CONDITION_SPECIFICATION,
        )
    elif entityType == EntityType.FURTHER_SPECIFICATION:
        return (
            EntityTag.B_FURTHER_SPECIFICATION,
            EntityTag.I_FURTHER_SPECIFICATION,
        )
    else:
        raise ValueError(f"EntityType: {entityType} not recognized")


def extract_entities(
    ner_tags: list[EntityTag], entity_type: EntityType, tokens: list[str]
) -> list[Entity]:
    begin_tag, inside_tag = get_tags(entity_type)
    entities = []
    current_entity = None
    for ner_tag, token, index in zip(ner_tags, tokens, range(len(ner_tags))):
        if ner_tag == begin_tag and ner_tags[index + 1] != inside_tag:
            entities.append(Entity(type=entity_type, start_index=index, tokens=[token]))
            current_entity = None
            continue
        if ner_tag == begin_tag and ner_tags[index + 1] == inside_tag:
            current_entity = Entity(type=entity_type, start_index=index, tokens=[token])
            continue
        if ner_tag == inside_tag and ner_tags[index + 1] == inside_tag:
            current_entity.tokens.append(token)
            continue
        if ner_tag == inside_tag and ner_tags[index + 1] != inside_tag:
            current_entity.tokens.append(token)
            entities.append(current_entity)
            current_entity = None

    return entities


def get_linear_index(sentence_ids: list[int], sid: int, wid: int) -> int:
    for sentence_id, index in zip(sentence_ids, range(len(sentence_ids))):
        if sid == sentence_id:
            result = index + wid
            return result if result < len(sentence_ids) else -1
    return -1


def find_entity_by_start_index(entities: list[Entity], start_index: int) -> Entity:
    for entity in entities:
        if entity.start_index == start_index:
            return entity


def extract_relations(
    source_head_sentence_ids: list[int],
    source_head_word_ids: list[int],
    types: list[str],
    target_head_sentence_ids: list[int],
    target_head_word_ids: list[int],
    sentence_ids: list[int],
    entities: list[Entity],
) -> list[Relation]:
    plain_relations = list(
        zip(
            source_head_sentence_ids,
            source_head_word_ids,
            types,
            target_head_sentence_ids,
            target_head_word_ids,
        )
    )

    relations = []
    for plain_relation in plain_relations:
        source_start_index = get_linear_index(
            sentence_ids=sentence_ids,
            sid=plain_relation[0],
            wid=plain_relation[1],
        )
        target_start_index = get_linear_index(
            sentence_ids=sentence_ids,
            sid=plain_relation[3],
            wid=plain_relation[4],
        )

        relation = Relation(
            type=str_to_relation_type(plain_relation[2]),
            source=find_entity_by_start_index(
                start_index=source_start_index, entities=entities
            ),
            target=find_entity_by_start_index(
                start_index=target_start_index, entities=entities
            ),
        )

        relations.append(relation)

    return relations


def plain_to_class(document) -> PetDocument:
    ner_tags = [str_to_entity_tag(ner_tag) for ner_tag in document["ner_tags"]]

    entities = []
    for entityType in EntityType:
        entities.extend(
            extract_entities(
                ner_tags=ner_tags, entity_type=entityType, tokens=document["tokens"]
            )
        )

    relations = extract_relations(
        source_head_sentence_ids=document["relations.source-head-sentence-ID"],
        source_head_word_ids=document["relations.source-head-word-ID"],
        types=document["relations.relation-type"],
        target_head_sentence_ids=document["relations.target-head-sentence-ID"],
        target_head_word_ids=document["relations.target-head-word-ID"],
        sentence_ids=document["sentence-IDs"],
        entities=entities,
    )

    return PetDocument(
        name=document["document name"],
        tokens=document["tokens"],
        ner_tags=ner_tags,
        relations=relations,
        entities=entities,
    )


class PetDataset:
    _instance = None
    _data = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PetDataset, cls).__new__(cls)
            df = pd.read_parquet("./data/pet_dataset.parquet")
            df["index"] = df["document name"]
            cls._data = df.sort_values(by="index")
        return cls._instance

    def get_document(self, document_number: int) -> PetDocument:
        document = self._data.iloc[document_number]
        return plain_to_class(document)

    def get_document_by_name(self, document_name: str) -> PetDocument:
        matching_rows = self._data[self._data["document name"] == document_name]
        document = matching_rows.iloc[0]
        return plain_to_class(document)

    def get_documents_by_name(self, document_names: list[str]) -> list[PetDocument]:
        documents = []
        for document_name in document_names:
            matching_rows = self._data[self._data["document name"] == document_name]
            if not matching_rows.empty:
                document = matching_rows.iloc[0]
                documents.append(plain_to_class(document))
        return documents
