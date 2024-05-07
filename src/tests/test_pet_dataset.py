from pet.pet_dataset import (
    PetDataset,
    extract_relations,
    get_linear_index,
    extract_entities,
)

from entity.entity_tag import EntityTag

from entity.entity_type import EntityType

from entity.entity import Entity

test_sentence_ids = [
    0,
    0,
    0,
    0,
    0,
    1,
    1,
    1,
    1,
    1,
    2,
    2,
    2,
    2,
    2,
    3,
    3,
    3,
    3,
    3,
    3,
    3,
    3,
    3,
    4,
    4,
    4,
    4,
]

test_ner_tags = [
    EntityTag.B_ACTOR,
    EntityTag.I_ACTOR,
    EntityTag.NO_ENTITY,
    EntityTag.NO_ENTITY,
    EntityTag.NO_ENTITY,
    EntityTag.NO_ENTITY,
    EntityTag.NO_ENTITY,
    EntityTag.B_ACTOR,
    EntityTag.NO_ENTITY,
    EntityTag.NO_ENTITY,
    EntityTag.NO_ENTITY,
    EntityTag.NO_ENTITY,
    EntityTag.NO_ENTITY,
]

test_tokens = [
    "An",
    "actor",
    "does",
    "something",
    "random",
    ".",
    "This",
    "actor",
    "has",
    "only",
    "one",
    "token",
    ".",
]

test_entities = [
    Entity(EntityType.ACTOR, 0, 1, ["An", "actor"]),
    Entity(EntityType.ACTOR, 7, 7, ["actor"]),
]


def test_get_document():
    dataset = PetDataset()
    document = dataset.get_document(42)
    assert (
        document.name
        and document.entities
        and document.relations
        and document.ner_tags
        and document.tokens
    )


def test_get_document_by_name():
    dataset = PetDataset()
    document = dataset.get_document_by_name("doc-10.1")
    assert (
        document.name == "doc-10.1"
        and document.entities
        and document.relations
        and document.ner_tags
        and document.tokens
    )


def test_get_linear_index():
    linear_index = get_linear_index(sentence_ids=test_sentence_ids, sid=3, wid=2)
    assert linear_index == 17


def test_extract_entities():
    extracted_entities = extract_entities(
        ner_tags=test_ner_tags, entity_type=EntityType.ACTOR, tokens=test_tokens
    )
    assert extracted_entities == test_entities


# def test_extract_relations():
#     extracted_relations = extract_relations()
