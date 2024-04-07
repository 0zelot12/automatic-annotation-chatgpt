from pet.pet_dataset import PetDataset


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
