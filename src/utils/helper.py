import json
import os

from metrics.entity_metrics import EntityMetrics, BaseMetrics

from metrics.relation_metrics import RelationMetrics
from entity.entity import Entity
from entity.entity_type import EntityType
from entity.entity_tag import EntityTag

from pet.pet_document import PetDocument
from relation.relation import Relation
from relation.relation_type import RelationType


# TODO: Move to entity.py
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


# TODO: Move to entity.py
def count_entities_of_type(entities: list[Entity], type: EntityType) -> int:
    result = 0
    for entity in entities:
        if entity.type == type:
            result += 1
    return result


def count_relations_of_type(relations: list[Relation], type: RelationType) -> int:
    result = 0
    for relation in relations:
        if relation.type == type:
            result += 1
    return result


def get_precision(true_postives: int, entities_recognized: int):
    return (
        0.0
        if true_postives == 0
        else round(
            true_postives / entities_recognized,
            2,
        )
    )


def get_recall(true_postives: int, entities_recognized_total: int):
    return (
        0.0
        if true_postives == 0
        else round(
            true_postives / entities_recognized_total,
            2,
        )
    )


def get_f1_score(precision: float, recall: float):
    return (
        0.0
        if precision == 0 and recall == 0.0
        else round(2 * precision * recall / (precision + recall), 2)
    )


def calculate_overall_metrics(
    entitiy_metrics: EntityMetrics, relations_metrics: RelationMetrics
) -> BaseMetrics:
    true_positives_entity = entitiy_metrics.overall.true_positives
    false_positives_entity = entitiy_metrics.overall.false_positives

    true_positives_relation = relations_metrics.overall.true_positives
    false_positives_relation = relations_metrics.overall.false_positives

    true_positives_total = true_positives_entity + true_positives_relation
    false_positives_total = false_positives_entity + false_positives_relation

    number_recognized_total = true_positives_total + false_positives_total
    reference_count_total = (
        entitiy_metrics.overall.reference_count
        + relations_metrics.overall.reference_count
    )

    precision = get_precision(true_positives_total, number_recognized_total)
    recall = get_recall(true_positives_total, reference_count_total)
    f1_score = get_f1_score(precision, recall)

    return BaseMetrics(
        precision,
        recall,
        f1_score,
        true_positives_total,
        false_positives_total,
        reference_count_total,
    )


# TODO: Move to some other file
def calculate_entity_metrics(
    model_entities: list[Entity], reference_entities: list[Entity]
) -> EntityMetrics:

    true_positives_overall = 0
    true_positives = {}
    for entity_type in EntityType:
        true_positives[entity_type] = 0

    for reference_annotation in reference_entities:
        found_element = next(
            (
                o
                for o in model_entities
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
            true_positives[found_element.type] += 1

    overall_precision = get_precision(true_positives_overall, len(model_entities))
    overall_recall = get_recall(true_positives_overall, len(reference_entities))
    overall_f1_score = get_f1_score(overall_precision, overall_recall)

    metrics = {}
    for entity_type in EntityType:
        entity_present = count_entities_of_type(reference_entities, entity_type)
        entity_recognized = count_entities_of_type(model_entities, entity_type)
        precision = get_precision(true_positives[entity_type], entity_recognized)
        recall = get_recall(true_positives[entity_type], entity_present)
        f1_score = get_f1_score(precision, recall)
        metrics[entity_type] = BaseMetrics(
            precision=precision,
            recall=recall,
            f1_score=f1_score,
            true_positives=true_positives[entity_type],
            false_positives=entity_recognized - true_positives[entity_type],
            reference_count=entity_present,
        )

    return EntityMetrics(
        overall=BaseMetrics(
            precision=overall_precision,
            recall=overall_recall,
            f1_score=overall_f1_score,
            true_positives=true_positives_overall,
            false_positives=len(model_entities) - true_positives_overall,
            reference_count=len(reference_entities),
        ),
        actor=metrics[EntityType.ACTOR],
        activity=metrics[EntityType.ACTIVITY],
        activity_data=metrics[EntityType.ACTIVITY_DATA],
        and_gateway=metrics[EntityType.AND_GATEWAY],
        xor_gateway=metrics[EntityType.XOR_GATEWAY],
        condition_specification=metrics[EntityType.CONDITION_SPECIFICATION],
        further_specification=metrics[EntityType.FURTHER_SPECIFICATION],
    )


def calculate_relation_metrics(
    model_relations: list[Relation], reference_relations: list[Relation]
) -> RelationMetrics:

    true_positives_overall = 0
    true_positives = {}

    for relation_type in RelationType:
        true_positives[relation_type] = 0

    for model_relation in model_relations:
        for reference_relation in reference_relations:
            if str(model_relation) == str(reference_relation):
                true_positives_overall += 1
                true_positives[model_relation.type] += 1

    overall_precision = get_precision(true_positives_overall, len(model_relations))
    overall_recall = get_recall(true_positives_overall, len(reference_relations))
    overall_f1_score = get_f1_score(overall_precision, overall_recall)

    metrics = {}
    for relation_type in RelationType:
        relation_present = count_relations_of_type(reference_relations, relation_type)
        relation_recognized = count_entities_of_type(model_relations, relation_type)
        precision = get_precision(true_positives[relation_type], relation_recognized)
        recall = get_recall(true_positives[relation_type], relation_present)
        f1_score = get_f1_score(precision, recall)
        metrics[relation_type] = BaseMetrics(
            precision=precision,
            recall=recall,
            f1_score=f1_score,
            true_positives=true_positives[relation_type],
            false_positives=relation_recognized - true_positives[relation_type],
            reference_count=relation_present,
        )

    return RelationMetrics(
        overall=BaseMetrics(
            precision=overall_precision,
            recall=overall_recall,
            f1_score=overall_f1_score,
            true_positives=true_positives_overall,
            false_positives=len(model_relations) - true_positives_overall,
            reference_count=len(reference_relations),
        ),
        actor_performer=metrics[RelationType.ACTOR_PERFORMER],
        actor_recipient=metrics[RelationType.ACTOR_RECIPIENT],
        flow=metrics[RelationType.FLOW],
        further_specification=metrics[RelationType.FURTHER_SPECIFICATION],
        same_gateway=metrics[RelationType.SAME_GATEWAY],
        uses=metrics[RelationType.USES],
    )


# TODO: Move to pet_document.py
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
