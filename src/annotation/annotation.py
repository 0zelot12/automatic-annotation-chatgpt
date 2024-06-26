from langchain.prompts import ChatPromptTemplate
from langchain.prompts import HumanMessagePromptTemplate
from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI

from metrics.annotation_metrics import AnnotationMetrics
from metrics.base_metrics import BaseMetrics

from pet.pet_document import PetDocument

from llm.templates import (
    entity_template,
    relation_template,
    relation_template_gold_standard,
)

from llm.utils import generate_model_entities, generate_model_relations, to_model_tokens

from annotation.annotation_result import AnnotationResult

from relation.relation import parse_relations

from entity.entity import parse_entities

from utils.helper import (
    calculate_entity_metrics,
    calculate_overall_metrics,
    calculate_relation_metrics,
)


def get_failure_annotation(
    document: PetDocument,
    training_documents: list[PetDocument],
    model_name: str,
    temperature: float,
) -> AnnotationResult:
    recognized_relations = []
    recognized_entities = []

    for relation in recognized_relations:
        recognized_entities.extend([relation.source, relation.target])
    recognized_entities = list(set(recognized_entities))

    entity_metrics = calculate_entity_metrics(
        model_entities=recognized_entities, reference_entities=document.entities
    )

    relation_metrics = calculate_relation_metrics(
        model_relations=recognized_relations, reference_relations=document.relations
    )

    overall_metrics = calculate_overall_metrics(entity_metrics, relation_metrics)

    return AnnotationResult(
        document_name=document.name,
        document_length=len(document.tokens),
        model=model_name,
        temperature=temperature,
        examples_documents=[document.name for document in training_documents],
        tokens=document.tokens,
        api_response="",
        context_length=[len(document.tokens) for document in training_documents],
        present_entities=document.entities,
        recognized_entities=recognized_entities,
        present_relations=document.relations,
        recognized_relations=recognized_relations,
        metrics=AnnotationMetrics(
            overall_metrics=overall_metrics,
            entity_metrics=entity_metrics,
            relation_metrics=relation_metrics,
        ),
    )


def annotate_relations(
    document: PetDocument,
    training_documents: list[PetDocument],
    model_name: str,
    temperature: float,
) -> AnnotationResult:
    chat_messages = [
        SystemMessage(
            content=(
                "You are an expert in the field of process management. You assist in annotating relevant entities "
                "and relations in natural language process descriptions. You will be provided with definitions of the "
                "entities and relations you need to extract."
            )
        )
    ]

    training_data = ""
    for training_document in training_documents:
        training_tokens = to_model_tokens(training_document.tokens)
        training_relations = generate_model_relations(training_document.relations)
        training_data += f"{training_tokens}\n{training_relations}\n"

    test_tokens = to_model_tokens(document.tokens)
    test_data = f"{test_tokens}"

    chat_messages.append(HumanMessagePromptTemplate.from_template(relation_template))

    template = ChatPromptTemplate.from_messages(
        chat_messages,
    )

    model = ChatOpenAI(model=model_name, temperature=temperature)
    chain = template | model

    api_response = chain.invoke(
        {"training_data": training_data, "test_data": test_data}
    )

    recognized_relations, relation_errors = parse_relations(
        relation_strings=api_response.content.splitlines(), tokens=document.tokens
    )

    recognized_entities = []
    for relation in recognized_relations:
        recognized_entities.extend([relation.source, relation.target])
    recognized_entities = list(set(recognized_entities))

    entity_metrics = calculate_entity_metrics(
        model_entities=recognized_entities, reference_entities=document.entities
    )

    relation_metrics = calculate_relation_metrics(
        model_relations=recognized_relations, reference_relations=document.relations
    )

    overall_metrics = calculate_overall_metrics(entity_metrics, relation_metrics)

    return AnnotationResult(
        document_name=document.name,
        document_length=len(document.tokens),
        model=model_name,
        temperature=temperature,
        errors=len(relation_errors),
        examples_documents=[document.name for document in training_documents],
        tokens=document.tokens,
        api_response=api_response.content,
        context_length=[len(document.tokens) for document in training_documents],
        present_entities=document.entities,
        recognized_entities=recognized_entities,
        present_relations=document.relations,
        recognized_relations=recognized_relations,
        metrics=AnnotationMetrics(
            overall_metrics=overall_metrics,
            entity_metrics=entity_metrics,
            relation_metrics=relation_metrics,
        ),
    )


def annotate_relations_with_gold_entities(
    document: PetDocument,
    training_documents: list[PetDocument],
    model_name: str,
    temperature: float,
) -> AnnotationResult:
    chat_messages = [
        SystemMessage(
            content=(
                "You are an expert in the field of process management. You assist in annotating relevant entities "
                "and relations in natural language process descriptions. You will be provided with definitions of the "
                "relations you need to extract and the entities that are present in the document."
            )
        )
    ]

    training_data = ""
    for training_document in training_documents:
        training_tokens = to_model_tokens(training_document.tokens)
        training_relations = generate_model_relations(training_document.relations)
        training_data += f"{training_tokens}\n{training_relations}\n"

    test_tokens = to_model_tokens(document.tokens)
    test_entities = generate_model_entities(document.entities)

    test_data = f"{test_tokens}\n{test_entities}"

    chat_messages.append(
        HumanMessagePromptTemplate.from_template(relation_template_gold_standard)
    )

    template = ChatPromptTemplate.from_messages(
        chat_messages,
    )

    model = ChatOpenAI(model=model_name, temperature=temperature)
    chain = template | model

    api_response = chain.invoke(
        {"training_data": training_data, "test_data": test_data}
    )

    recognized_relations, relation_errors = parse_relations(
        relation_strings=api_response.content.splitlines(), tokens=document.tokens
    )

    relation_metrics = calculate_relation_metrics(
        model_relations=recognized_relations, reference_relations=document.relations
    )

    return AnnotationResult(
        document_name=document.name,
        document_length=len(document.tokens),
        model=model_name,
        temperature=temperature,
        examples_documents=[document.name for document in training_documents],
        tokens=document.tokens,
        context_length=[len(document.tokens) for document in training_documents],
        errors=len(relation_errors),
        api_response=api_response.content,
        present_entities=document.entities,
        recognized_entities=[],
        present_relations=document.relations,
        recognized_relations=recognized_relations,
        metrics=AnnotationMetrics(
            overall_metrics=BaseMetrics(
                f1_score=-1.0,
                precision=-1.0,
                recall=-1.0,
                true_positives=-1.0,
                false_positives=-1.0,
                reference_count=-1.0,
            ),
            entity_metrics=BaseMetrics(
                f1_score=-1.0,
                precision=-1.0,
                recall=-1.0,
                true_positives=-1.0,
                false_positives=-1.0,
                reference_count=-1.0,
            ),
            relation_metrics=relation_metrics,
        ),
    )


def annotate_relations_with_entities(
    document: PetDocument,
    training_documents: list[PetDocument],
    model_name: str,
    temperature: float,
) -> AnnotationResult:

    entity_metrics, recognized_entities = annotate_entities(
        document=document,
        model_name=model_name,
        training_documents=training_documents,
        temperature=temperature,
    )

    chat_messages = [
        SystemMessage(
            content=(
                "You are an expert in the field of process management. You assist in annotating relevant entities "
                "and relations in natural language process descriptions. You will be provided with definitions of the "
                "relations you need to extract and the entities that are present in the document."
            )
        )
    ]

    training_data = ""
    for training_document in training_documents:
        training_tokens = to_model_tokens(training_document.tokens)
        training_relations = generate_model_relations(training_document.relations)
        training_data += f"{training_tokens}\n{training_relations}\n"

    test_tokens = to_model_tokens(document.tokens)
    test_entities = generate_model_entities(recognized_entities)

    test_data = f"{test_tokens}\n{test_entities}"

    chat_messages.append(
        HumanMessagePromptTemplate.from_template(relation_template_gold_standard)
    )

    template = ChatPromptTemplate.from_messages(
        chat_messages,
    )

    model = ChatOpenAI(model=model_name, temperature=temperature)
    chain = template | model

    api_response = chain.invoke(
        {"training_data": training_data, "test_data": test_data}
    )

    recognized_relations, relation_errors = parse_relations(
        relation_strings=api_response.content.splitlines(), tokens=document.tokens
    )

    relation_metrics = calculate_relation_metrics(
        model_relations=recognized_relations, reference_relations=document.relations
    )

    overall_metrics = calculate_overall_metrics(entity_metrics, relation_metrics)

    return AnnotationResult(
        document_name=document.name,
        document_length=len(document.tokens),
        model=model_name,
        temperature=temperature,
        examples_documents=[document.name for document in training_documents],
        tokens=document.tokens,
        context_length=[len(document.tokens) for document in training_documents],
        api_response=api_response.content,
        errors=len(relation_errors),
        present_entities=document.entities,
        recognized_entities=recognized_entities,
        present_relations=document.relations,
        recognized_relations=recognized_relations,
        metrics=AnnotationMetrics(
            overall_metrics=overall_metrics,
            entity_metrics=entity_metrics,
            relation_metrics=relation_metrics,
        ),
    )


def annotate_entities(
    document: PetDocument,
    training_documents: list[PetDocument],
    model_name: str,
    temperature: float,
):
    chat_messages = [
        SystemMessage(
            content=(
                "You are an expert in the field of process management. You assist in annotating relevant entities "
                "and relations in natural language process descriptions. You will be provided with definitions of the "
                "entities you need to extract."
            )
        )
    ]

    training_data = ""
    for training_document in training_documents:
        training_tokens = to_model_tokens(training_document.tokens)
        training_entities = generate_model_entities(training_document.entities)
        training_data += f"{training_tokens}\n{training_entities}\n"

    test_tokens = to_model_tokens(document.tokens)

    test_data = f"{test_tokens}"

    chat_messages.append(HumanMessagePromptTemplate.from_template(entity_template))

    template = ChatPromptTemplate.from_messages(
        chat_messages,
    )

    model = ChatOpenAI(model=model_name, temperature=temperature)
    chain = template | model

    api_response = chain.invoke(
        {"training_data": training_data, "test_data": test_data}
    )

    recognized_entities = parse_entities(
        entity_strings=api_response.content.splitlines(), tokens=document.tokens
    )

    entity_metrics = calculate_entity_metrics(
        model_entities=recognized_entities, reference_entities=document.entities
    )

    return entity_metrics, recognized_entities
