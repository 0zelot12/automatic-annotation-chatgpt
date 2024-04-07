from pet.pet_dataset import PetDataset, get_linear_index

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


def test_singleton_instance():
    dataset = PetDataset()
    another_dataset = PetDataset()
    assert dataset == another_dataset


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
        document.name
        and document.entities
        and document.relations
        and document.ner_tags
        and document.tokens
    )


def test_get_linear_index():
    linear_index = get_linear_index(sentence_ids=test_sentence_ids, sid=3, wid=2)
    assert linear_index == 17
