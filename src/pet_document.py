from dataclasses import dataclass

from entity_tag import EntityTag
from entity import Entity
from entity_type import EntityType


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

    # TODO: Refactor entity methods

    def get_actors(self) -> list[Entity]:
        actors = []
        current_actor = None
        for ner_tag, token, index in zip(
            self.ner_tags, self.tokens, range(len(self.ner_tags))
        ):
            if (
                ner_tag == EntityTag.B_ACTOR
                and self.ner_tags[index + 1] != EntityTag.I_ACTOR
            ):
                actors.append(
                    Entity(type=EntityType.ACTOR, start_index=index, tokens=[token])
                )
                current_actor = None
                continue
            if (
                ner_tag == EntityTag.B_ACTOR
                and self.ner_tags[index + 1] == EntityTag.I_ACTOR
            ):
                current_actor = Entity(
                    type=EntityType.ACTOR, start_index=index, tokens=[token]
                )
                continue
            if (
                ner_tag == EntityTag.I_ACTOR
                and self.ner_tags[index + 1] == EntityTag.I_ACTOR
            ):
                current_actor.tokens.append(token)
                continue
            if (
                ner_tag == EntityTag.I_ACTOR
                and self.ner_tags[index + 1] != EntityTag.I_ACTOR
            ):
                current_actor.tokens.append(token)
                actors.append(current_actor)
                current_actor = None

        return actors

    def get_activites(self) -> list[Entity]:
        activities = []
        current_activity = None
        for ner_tag, token, index in zip(
            self.ner_tags, self.tokens, range(len(self.ner_tags))
        ):
            if (
                ner_tag == EntityTag.B_ACTIVITY
                and self.ner_tags[index + 1] != EntityTag.I_ACTIVITY
            ):
                activities.append(
                    Entity(type=EntityType.ACTIVITY, start_index=index, tokens=[token])
                )
                current_activity = None
                continue
            if (
                ner_tag == EntityTag.B_ACTIVITY
                and self.ner_tags[index + 1] == EntityTag.I_ACTIVITY
            ):
                current_activity = Entity(
                    type=EntityType.ACTIVITY, start_index=index, tokens=[token]
                )
                continue
            if (
                ner_tag == EntityTag.I_ACTIVITY
                and self.ner_tags[index + 1] == EntityTag.I_ACTIVITY
            ):
                current_activity.tokens.append(token)
                continue
            if (
                ner_tag == EntityTag.I_ACTIVITY
                and self.ner_tags[index + 1] != EntityTag.I_ACTIVITY
            ):
                current_activity.tokens.append(token)
                activities.append(current_activity)
                current_activity = None

        return activities

    def get_activity_data(self) -> list[Entity]:
        activity_data = []
        current_activity_data = None
        for ner_tag, token, index in zip(
            self.ner_tags, self.tokens, range(len(self.ner_tags))
        ):
            if (
                ner_tag == EntityTag.B_ACTIVITY_DATA
                and self.ner_tags[index + 1] != EntityTag.I_ACTIVITY_DATA
            ):
                activity_data.append(
                    Entity(
                        type=EntityType.ACTIVITY_DATA, start_index=index, tokens=[token]
                    )
                )
                current_activity_data = None
                continue
            if (
                ner_tag == EntityTag.B_ACTIVITY_DATA
                and self.ner_tags[index + 1] == EntityTag.I_ACTIVITY_DATA
            ):
                current_activity_data = Entity(
                    type=EntityType.ACTIVITY_DATA, start_index=index, tokens=[token]
                )
                continue
            if (
                ner_tag == EntityTag.I_ACTIVITY_DATA
                and self.ner_tags[index + 1] == EntityTag.I_ACTIVITY_DATA
            ):
                current_activity_data.tokens.append(token)
                continue
            if (
                ner_tag == EntityTag.I_ACTIVITY_DATA
                and self.ner_tags[index + 1] != EntityTag.I_ACTIVITY_DATA
            ):
                current_activity_data.tokens.append(token)
                activity_data.append(current_activity_data)
                current_activity_data = None

        return activity_data

    def get_entities(self) -> list[Entity]:
        entities = self.get_actors() + self.get_activites() + self.get_activity_data()
        return sorted(entities, key=lambda x: x.start_index)
