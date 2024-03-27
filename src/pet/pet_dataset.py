import platform

import pandas as pd

from entity.entity import Entity
from entity.entity_type import EntityType
from pet.pet_document import PetDocument

from entity.entity_tag import EntityTag, str_to_entity
from relation.relation import Relation, str_to_type


def get_actors(ner_tags: list[EntityTag], tokens: list[str]) -> list[Entity]:
    actors = []
    current_actor = None
    for ner_tag, token, index in zip(ner_tags, tokens, range(len(ner_tags))):
        if ner_tag == EntityTag.B_ACTOR and ner_tags[index + 1] != EntityTag.I_ACTOR:
            actors.append(
                Entity(type=EntityType.ACTOR, start_index=index, tokens=[token])
            )
            current_actor = None
            continue
        if ner_tag == EntityTag.B_ACTOR and ner_tags[index + 1] == EntityTag.I_ACTOR:
            current_actor = Entity(
                type=EntityType.ACTOR, start_index=index, tokens=[token]
            )
            continue
        if ner_tag == EntityTag.I_ACTOR and ner_tags[index + 1] == EntityTag.I_ACTOR:
            current_actor.tokens.append(token)
            continue
        if ner_tag == EntityTag.I_ACTOR and ner_tags[index + 1] != EntityTag.I_ACTOR:
            current_actor.tokens.append(token)
            actors.append(current_actor)
            current_actor = None

    return actors


def get_activites(ner_tags: list[EntityTag], tokens: list[str]) -> list[Entity]:
    activities = []
    current_activity = None
    for ner_tag, token, index in zip(ner_tags, tokens, range(len(ner_tags))):
        if (
            ner_tag == EntityTag.B_ACTIVITY
            and ner_tags[index + 1] != EntityTag.I_ACTIVITY
        ):
            activities.append(
                Entity(type=EntityType.ACTIVITY, start_index=index, tokens=[token])
            )
            current_activity = None
            continue
        if (
            ner_tag == EntityTag.B_ACTIVITY
            and ner_tags[index + 1] == EntityTag.I_ACTIVITY
        ):
            current_activity = Entity(
                type=EntityType.ACTIVITY, start_index=index, tokens=[token]
            )
            continue
        if (
            ner_tag == EntityTag.I_ACTIVITY
            and ner_tags[index + 1] == EntityTag.I_ACTIVITY
        ):
            current_activity.tokens.append(token)
            continue
        if (
            ner_tag == EntityTag.I_ACTIVITY
            and ner_tags[index + 1] != EntityTag.I_ACTIVITY
        ):
            current_activity.tokens.append(token)
            activities.append(current_activity)
            current_activity = None

    return activities


def get_activity_data(ner_tags: list[EntityTag], tokens: list[str]) -> list[Entity]:
    activity_data = []
    current_activity_data = None
    for ner_tag, token, index in zip(ner_tags, tokens, range(len(ner_tags))):
        if (
            ner_tag == EntityTag.B_ACTIVITY_DATA
            and ner_tags[index + 1] != EntityTag.I_ACTIVITY_DATA
        ):
            activity_data.append(
                Entity(type=EntityType.ACTIVITY_DATA, start_index=index, tokens=[token])
            )
            current_activity_data = None
            continue
        if (
            ner_tag == EntityTag.B_ACTIVITY_DATA
            and ner_tags[index + 1] == EntityTag.I_ACTIVITY_DATA
        ):
            current_activity_data = Entity(
                type=EntityType.ACTIVITY_DATA, start_index=index, tokens=[token]
            )
            continue
        if (
            ner_tag == EntityTag.I_ACTIVITY_DATA
            and ner_tags[index + 1] == EntityTag.I_ACTIVITY_DATA
        ):
            current_activity_data.tokens.append(token)
            continue
        if (
            ner_tag == EntityTag.I_ACTIVITY_DATA
            and ner_tags[index + 1] != EntityTag.I_ACTIVITY_DATA
        ):
            current_activity_data.tokens.append(token)
            activity_data.append(current_activity_data)
            current_activity_data = None

    return activity_data


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
            type=str_to_type(plain_relation[2]),
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
    # Convert ner-tags
    ner_tags = [str_to_entity(ner_tag) for ner_tag in document["ner_tags"]]

    # Convert entities
    entities = (
        get_actors(ner_tags=ner_tags, tokens=document["tokens"])
        + get_activites(ner_tags=ner_tags, tokens=document["tokens"])
        + get_activity_data(ner_tags=ner_tags, tokens=document["tokens"])
    )

    # Convert relations
    relations = None
    # TODO: Check why this is needed
    if platform.system() == "Windows":
        relations = extract_relations(
            source_head_sentence_ids=document["relations"]["source-head-sentence-ID"],
            source_head_word_ids=document["relations"]["source-head-word-ID"],
            types=document["relations"]["relation-type"],
            target_head_sentence_ids=document["relations"]["target-head-sentence-ID"],
            target_head_word_ids=document["relations"]["target-head-word-ID"],
            sentence_ids=document["sentence-IDs"],
            entities=entities,
        )
    else:
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
