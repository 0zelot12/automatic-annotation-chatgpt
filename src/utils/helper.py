import pickle

import numpy as np

from datetime import datetime

from metrics.entity_metrics import EntityMetrics, BaseMetrics

from metrics.relation_metrics import RelationMetrics

from entity.entity import Entity
from entity.entity_type import EntityType

from relation.relation import Relation
from relation.relation_type import RelationType


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


def calculate_entity_partial(
    model_entities: list[Entity], reference_entities: list[Entity]
) -> EntityMetrics:

    true_positives_overall = 0
    true_positives = {}
    for entity_type in EntityType:
        true_positives[entity_type] = 0

    for gold_entity in reference_entities:
        index_range_gold = gold_entity.get_index_range()
        for entity in model_entities:
            index_range = entity.get_index_range()
            intersection = np.intersect1d(index_range, index_range_gold)
            if entity.type == gold_entity.type and len(intersection) > 1:
                true_positives_overall += 1
                true_positives[entity.type] += 1

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


def split_list(lst, n):
    if n <= 0:
        raise ValueError("Number of splits must be greater than 0")

    chunk_size = len(lst) // n
    remainder = len(lst) % n

    sizes = [chunk_size + 1 if i < remainder else chunk_size for i in range(n)]

    result = [lst[sum(sizes[:i]) : sum(sizes[: i + 1])] for i in range(n)]

    return result


def k_fold(data: list, k: int):
    np.random.seed(42)
    np.random.shuffle(data)
    return split_list(data, k)


def save_to_file(
    path: str,
    file_name: str,
    data: any,
) -> None:
    with open(
        f"./out/{file_name}-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.pickle",
        "wb",
    ) as f:
        pickle.dump(data, f)
