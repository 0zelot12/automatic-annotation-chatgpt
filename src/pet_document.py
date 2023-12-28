from dataclasses import dataclass


@dataclass
class PetDocument:
    name: str
    tokens: list[str]
    ner_tags: list[str]
