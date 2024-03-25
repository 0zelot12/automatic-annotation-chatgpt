from dataclasses import dataclass

from entity_tag import EntityTag
from entity import Entity
from entity_type import EntityType
from relation import Relation


@dataclass
class PetDocument:
    """
    Represents a document of the PET dataset.

    Attributes:
        name (str): The name of the document.
        tokens (list of str): A list of tokens representing the content of the document.
        ner_tags (list of str): A list of named entity recognition (NER) tags associated with the document.
    """

    name: str
    tokens: list[str]
    ner_tags: list[EntityTag]
    relations: list[Relation]
    entities: list[Entity]
