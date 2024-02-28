from entity import Entity
from entity_type import EntityType

from entity_tag import EntityTag


def parse_entities(response: list[str]) -> list[Entity]:
    entities = []
    current_entity = None
    offset = 0
    for r, i in zip(response, range(0, len(response))):
        if r == "<ACTOR>":
            offset += 1
            current_entity = Entity(
                type=EntityType.ACTOR, start_index=(i - offset) + 1, tokens=[]
            )
            continue
        if r == "</ACTOR>":
            offset += 1
            entities.append(current_entity)
            current_entity = None
            continue
        if r == "<ACTIVITY>":
            offset += 1
            current_entity = Entity(
                type=EntityType.ACTIVITY, start_index=(i - offset) + 1, tokens=[]
            )
            continue
        if r == "</ACTIVITY>":
            offset += 1
            entities.append(current_entity)
            current_entity = None
            continue
        if r == "<ACTIVITY_DATA>":
            offset += 1
            current_entity = Entity(
                type=EntityType.ACTIVITY_DATA, start_index=(i - offset) + 1, tokens=[]
            )
            continue
        if r == "</ACTIVITY_DATA>":
            offset += 1
            entities.append(current_entity)
            current_entity = None
            continue
        if current_entity:
            current_entity.tokens.append(r)
    return entities


def convert_to_template_example(
    tokens: list[str], ner_tags: list[EntityTag]
) -> list[str]:
    result = []
    for token, ner_tag, index in zip(tokens, ner_tags, range(len(tokens))):

        # ACTOR
        if ner_tag == EntityTag.B_ACTOR and ner_tags[index + 1] == EntityTag.I_ACTOR:
            result.append("<ACTOR>")
            result.append(f"{token}")
            continue
        if ner_tag == EntityTag.B_ACTOR and ner_tags[index + 1] != EntityTag.I_ACTOR:
            result.append("<ACTOR>")
            result.append(f"{token}")
            result.append("</ACTOR>")
            continue
        if ner_tag == EntityTag.I_ACTOR and ner_tags[index + 1] == EntityTag.I_ACTOR:
            result.append(f"{token}")
            continue
        if ner_tag == EntityTag.I_ACTOR and ner_tags[index + 1] != EntityTag.I_ACTOR:
            result.append(f"{token}")
            result.append("</ACTOR>")
            continue

        # ACTIVITY
        if (
            ner_tag == EntityTag.B_ACTIVITY
            and ner_tags[index + 1] == EntityTag.I_ACTIVITY
        ):
            result.append("<ACTIVITY>")
            result.append(f"{token}")
            continue
        if (
            ner_tag == EntityTag.B_ACTIVITY
            and ner_tags[index + 1] != EntityTag.I_ACTIVITY
        ):
            result.append("<ACTIVITY>")
            result.append(f"{token}")
            result.append("</ACTIVITY>")
            continue
        if (
            ner_tag == EntityTag.I_ACTIVITY
            and ner_tags[index + 1] == EntityTag.I_ACTIVITY
        ):
            result.append(f"{token}")
            continue
        if (
            ner_tag == EntityTag.I_ACTIVITY
            and ner_tags[index + 1] != EntityTag.I_ACTIVITY
        ):
            result.append(f"{token}")
            result.append("</ACTIVITY>")
            continue

        # ACTIVITY_DATA
        if (
            ner_tag == EntityTag.B_ACTIVITY_DATA
            and ner_tags[index + 1] == EntityTag.I_ACTIVITY_DATA
        ):
            result.append("<ACTIVITY_DATA>")
            result.append(f"{token}")
            continue
        if (
            ner_tag == EntityTag.B_ACTIVITY_DATA
            and ner_tags[index + 1] != EntityTag.I_ACTIVITY_DATA
        ):
            result.append("<ACTIVITY_DATA>")
            result.append(f"{token}")
            result.append("</ACTIVITY_DATA>")
            continue
        if (
            ner_tag == EntityTag.I_ACTIVITY_DATA
            and ner_tags[index + 1] == EntityTag.I_ACTIVITY_DATA
        ):
            result.append(f"{token}")
            continue
        if (
            ner_tag == EntityTag.I_ACTIVITY_DATA
            and ner_tags[index + 1] != EntityTag.I_ACTIVITY_DATA
        ):
            result.append(f"{token}")
            result.append("</ACTIVITY_DATA>")
            continue

        # NO_ENTITY
        if ner_tag == EntityTag.NO_ENTITY:
            result.append(f"{token}")
            continue

    return result


def calculate_metrics(
    model_annotations: list[Entity], reference_annotations: list[Entity]
):
    true_positives = 0
    false_negatives = 0
    for reference_annotation in reference_annotations:
        found_element = next(
            (
                o
                for o in model_annotations
                if o.start_index == reference_annotation.start_index
            ),
            None,
        )
        if found_element and reference_annotation.tokens == found_element.tokens:
            true_positives += 1
        else:
            false_negatives += 1

    precision = true_positives / len(model_annotations)
    recall = true_positives / len(reference_annotations)

    if precision + recall == 0:
        return [
            precision,
            recall,
            -1,
        ]  # TODO: Clarify what to return when precision + recall = 0

    f1_score = round(2 * precision * recall / (precision + recall), 2)

    return [precision, recall, f1_score]
