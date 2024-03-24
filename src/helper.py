from annotation_metrics import AnnotationMetrics

from entity import Entity
from entity_type import EntityType
from entity_tag import EntityTag

import json
import os

from pet_document import PetDocument


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


def count_entities_of_type(entities: list[Entity], type: EntityType) -> int:
    result = 0
    for entity in entities:
        if entity.type == type:
            result += 1
    return result


def calculate_metrics(
    model_annotations: list[Entity], reference_annotations: list[Entity]
) -> AnnotationMetrics:
    true_positives_overall = 0
    true_positives_actor = 0
    true_positives_activity = 0
    true_positives_activity_data = 0
    for reference_annotation in reference_annotations:
        found_element = next(
            (
                o
                for o in model_annotations
                if o.start_index == reference_annotation.start_index
            ),
            None,
        )
        if (
            found_element
            and reference_annotation.tokens == found_element.tokens
            and reference_annotation.type == found_element.type
        ):
            true_positives_overall += 1
            if found_element.type == EntityType.ACTOR:
                true_positives_actor += 1
            if found_element.type == EntityType.ACTIVITY:
                true_positives_activity += 1
            if found_element.type == EntityType.ACTIVITY_DATA:
                true_positives_activity_data += 1

    precision = round(true_positives_overall / len(model_annotations), 2)
    recall = round(true_positives_overall / len(reference_annotations), 2)

    # Metrics ACTOR

    actor_precision = round(
        true_positives_actor
        / count_entities_of_type(model_annotations, EntityType.ACTOR),
        2,
    )

    actor_recall = round(
        true_positives_actor
        / count_entities_of_type(reference_annotations, EntityType.ACTOR),
        2,
    )

    actor_f1_score = (
        0.0
        if actor_precision + actor_recall == 0.0
        else round(
            2 * actor_precision * actor_recall / (actor_precision + actor_recall), 2
        )
    )

    # Metrics ACTIVITY

    activity_precision = round(
        true_positives_activity
        / count_entities_of_type(model_annotations, EntityType.ACTIVITY),
        2,
    )

    activity_recall = round(
        true_positives_activity
        / count_entities_of_type(reference_annotations, EntityType.ACTIVITY),
        2,
    )

    activity_f1_score = (
        0.0
        if activity_precision + activity_recall == 0.0
        else round(
            2
            * activity_precision
            * activity_recall
            / (activity_precision + activity_recall),
            2,
        )
    )

    # Metrics ACTIVITY_DATA

    activity_data_precision = round(
        true_positives_activity_data
        / count_entities_of_type(model_annotations, EntityType.ACTIVITY_DATA),
        2,
    )

    activity_data_recall = round(
        true_positives_activity_data
        / count_entities_of_type(reference_annotations, EntityType.ACTIVITY_DATA),
        2,
    )

    activity_data_f1_score = (
        0.0
        if activity_data_precision + activity_data_recall == 0.0
        else round(
            2
            * activity_data_precision
            * activity_data_recall
            / (activity_data_precision + activity_data_recall),
            2,
        )
    )

    if precision + recall == 0:
        return AnnotationMetrics(precision=precision, recall=recall, f1_score=0.0)

    f1_score = round(2 * precision * recall / (precision + recall), 2)

    return AnnotationMetrics(
        precision=precision,
        recall=recall,
        f1_score=f1_score,
        actor_precision=actor_precision,
        actor_recall=actor_recall,
        actor_f1_score=actor_f1_score,
        activity_precision=activity_precision,
        activity_recall=activity_recall,
        activity_f1_score=activity_f1_score,
        activity_data_precision=activity_data_precision,
        activity_data_recall=activity_data_recall,
        activity_data_f1_score=activity_data_f1_score,
    )


# TODO: Move to PetDocument class
def convert_to_template_example(document: PetDocument) -> list[str]:
    result = []
    for token, ner_tag, index in zip(
        document.tokens, document.ner_tags, range(len(document.tokens))
    ):

        # ACTOR
        if (
            ner_tag == EntityTag.B_ACTOR
            and document.ner_tags[index + 1] == EntityTag.I_ACTOR
        ):
            result.append("<ACTOR>")
            result.append(f"{token}")
            continue
        if (
            ner_tag == EntityTag.B_ACTOR
            and document.ner_tags[index + 1] != EntityTag.I_ACTOR
        ):
            result.append("<ACTOR>")
            result.append(f"{token}")
            result.append("</ACTOR>")
            continue
        if (
            ner_tag == EntityTag.I_ACTOR
            and document.ner_tags[index + 1] == EntityTag.I_ACTOR
        ):
            result.append(f"{token}")
            continue
        if (
            ner_tag == EntityTag.I_ACTOR
            and document.ner_tags[index + 1] != EntityTag.I_ACTOR
        ):
            result.append(f"{token}")
            result.append("</ACTOR>")
            continue

        # ACTIVITY
        if (
            ner_tag == EntityTag.B_ACTIVITY
            and document.ner_tags[index + 1] == EntityTag.I_ACTIVITY
        ):
            result.append("<ACTIVITY>")
            result.append(f"{token}")
            continue
        if (
            ner_tag == EntityTag.B_ACTIVITY
            and document.ner_tags[index + 1] != EntityTag.I_ACTIVITY
        ):
            result.append("<ACTIVITY>")
            result.append(f"{token}")
            result.append("</ACTIVITY>")
            continue
        if (
            ner_tag == EntityTag.I_ACTIVITY
            and document.ner_tags[index + 1] == EntityTag.I_ACTIVITY
        ):
            result.append(f"{token}")
            continue
        if (
            ner_tag == EntityTag.I_ACTIVITY
            and document.ner_tags[index + 1] != EntityTag.I_ACTIVITY
        ):
            result.append(f"{token}")
            result.append("</ACTIVITY>")
            continue

        # ACTIVITY_DATA
        if (
            ner_tag == EntityTag.B_ACTIVITY_DATA
            and document.ner_tags[index + 1] == EntityTag.I_ACTIVITY_DATA
        ):
            result.append("<ACTIVITY_DATA>")
            result.append(f"{token}")
            continue
        if (
            ner_tag == EntityTag.B_ACTIVITY_DATA
            and document.ner_tags[index + 1] != EntityTag.I_ACTIVITY_DATA
        ):
            result.append("<ACTIVITY_DATA>")
            result.append(f"{token}")
            result.append("</ACTIVITY_DATA>")
            continue
        if (
            ner_tag == EntityTag.I_ACTIVITY_DATA
            and document.ner_tags[index + 1] == EntityTag.I_ACTIVITY_DATA
        ):
            result.append(f"{token}")
            continue
        if (
            ner_tag == EntityTag.I_ACTIVITY_DATA
            and document.ner_tags[index + 1] != EntityTag.I_ACTIVITY_DATA
        ):
            result.append(f"{token}")
            result.append("</ACTIVITY_DATA>")
            continue

        # NO_ENTITY
        if ner_tag == EntityTag.NO_ENTITY:
            result.append(f"{token}")
            continue

    return result


def avg(values: list[float]) -> float:
    return round(sum(values) / len(values), 2)


def evaluate_results(path: str):
    # TODO: Add test
    data = []
    for filename in os.listdir(path):
        if filename.endswith(".json"):
            filepath = os.path.join(path, filename)
            with open(filepath, "r") as file:
                json_data = json.load(file)
                data.append(json_data)

    plot_data = []

    for d in data:
        plot_data.append(
            {
                "recall": d["metrics"]["recall"],
                "precision": d["metrics"]["precision"],
                "f1_score": d["metrics"]["f1_score"],
            }
        )

    # Extract recall and precision values from the data
    recalls = [d["recall"] for d in plot_data]
    precisions = [d["precision"] for d in plot_data]
    f1_scores = [d["f1_score"] for d in plot_data]

    print(f"Average Recall: {avg(recalls)}")
    print(f"Maximum Recall: {max(recalls)}")
    print(f"Minimum Recall: {min(recalls)}")
    print("----------------------------------------------------")
    print(f"Average Precision: {avg(precisions)}")
    print(f"Maximum Precision: {max(precisions)}")
    print(f"Minimum Precision: {min(precisions)}")
    print("----------------------------------------------------")
    print(f"Average F1-score: {avg(f1_scores)}")
    print(f"Maximum F1-score: {max(f1_scores)}")
    print(f"Minimum F1-score: {min(f1_scores)}")
