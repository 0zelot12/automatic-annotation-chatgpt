from dataclasses import dataclass

from entity import Entity


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
    ner_tags: list[Entity]

    def get_actors(self) -> list[str]:
        actors = []
        current_actor = []
        for ner_tag, token, index in zip(
            self.ner_tags, self.tokens, range(len(self.ner_tags))
        ):
            if (
                ner_tag == Entity.B_ACTOR and self.ner_tags[index + 1] != Entity.I_ACTOR
            ):  # Actor if length one
                actors.append([token])
                current_actor = []
                continue
            if ner_tag == Entity.B_ACTOR and self.ner_tags[index + 1] == Entity.I_ACTOR:
                current_actor.append(token)
                continue
            if ner_tag == Entity.I_ACTOR and self.ner_tags[index + 1] == Entity.I_ACTOR:
                current_actor.append(token)
                continue
            if ner_tag == Entity.I_ACTOR and self.ner_tags[index + 1] != Entity.I_ACTOR:
                current_actor.append(token)
                actors.append(current_actor)
                current_actor = []
        return actors
