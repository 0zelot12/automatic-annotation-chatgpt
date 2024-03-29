from dataclasses import dataclass, field

from entity.entity_tag import EntityTag
from entity.entity import Entity
from relation.relation import Relation


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
    tokens: list[str] = field(default_factory=list)
    ner_tags: list[EntityTag] = field(default_factory=list)
    relations: list[Relation] = field(default_factory=list)
    entities: list[Entity] = field(default_factory=list)

    def to_json(self):
        return {
            "document_name": self.name,
            "tokens": [str(token) for token in self.tokens],
            "ner_tags": [str(ner_tag) for ner_tag in self.ner_tags],
            "relations": [relation.to_json() for relation in self.relations],
            "entities": [entity.to_json() for entity in self.entities],
        }
