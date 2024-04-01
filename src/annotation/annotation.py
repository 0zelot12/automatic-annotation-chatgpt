import logging

from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import HumanMessagePromptTemplate
from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI

from annotation.annotation_metrics import AnnotationMetrics
from metrics.metrics import Metrics
from pet.pet_document import PetDocument

from llm.templates import (
    zero_shot_template_base,
    one_shot_template_base,
    few_shot_template_base,
    relation_template,
)

from llm.utils import generate_model_relations, to_model_tokens

from annotation.annotation_result import AnnotationResult
from llm.model_response import ModelResponse

from relation.relation import parse_relations
from utils.helper import (
    calculate_entity_metrics,
    calculate_relation_metrics,
    parse_entities,
    convert_to_template_example,
)


def annotate_relations(
    document: PetDocument,
    example_document: PetDocument,
    model_name: str,
    prompt_type: str,
    temperature: float,
) -> AnnotationResult:
    chat_messages = [
        SystemMessage(
            content=(
                "You are an expert in the field of process management. You assist in annotating relevant entities "
                "and relations in natural language process descriptions. You will be provided with definitions of the entities you need to extract."
            )
        )
    ]

    training_tokens = to_model_tokens(example_document.tokens)
    training_relations = generate_model_relations(example_document.relations)

    test_tokens = to_model_tokens(document.tokens)
    test_relations = generate_model_relations(document.relations)

    training_data = f"{training_tokens}\n{training_relations}"
    test_data = f"{test_tokens}\n{test_relations}"

    chat_messages.append(HumanMessagePromptTemplate.from_template(relation_template))

    template = ChatPromptTemplate.from_messages(
        chat_messages,
    )

    model = ChatOpenAI(model=model_name, temperature=temperature)
    chain = template | model

    api_response = chain.invoke(
        {"training_data": training_data, "test_data": test_data}
    )

    recognized_relations = parse_relations(
        relation_strings=api_response.content.splitlines(), tokens=document.tokens
    )

    recognized_entities = []
    for relation in recognized_relations:
        recognized_entities.extend([relation.source, relation.target])
    recognized_entities = set(recognized_entities)

    return AnnotationResult(
        document_name=document.name,
        document_length=len(document.tokens),
        prompt_type=prompt_type,
        temperature=temperature,
        examples_documents=[example_document.name],
        tokens=document.tokens,
        api_response=api_response.content,
        present_entities=document.entities,
        recognized_entities=recognized_entities,
        present_relations=document.relations,
        recognized_relations=recognized_relations,
        metrics=AnnotationMetrics(
            overall_metrics=Metrics(
                precision=0,
                recall=0,
                f1_score=0,
                true_positives=0,
                false_positives=0,
                reference_count=0,
            ),
            entity_metrics=calculate_entity_metrics(
                model_entities=recognized_entities, reference_entities=document.entities
            ),
            relation_metrics=calculate_relation_metrics(
                model_relations=recognized_relations,
                reference_relations=document.relations,
            ),
        ),
    )


def annotate_document(
    document: PetDocument,
    example_document_1: PetDocument,
    example_document_2: PetDocument,
    model_name: str,
    prompt_type: str,
    temperature: float,
) -> AnnotationResult:

    chat_template = generate_prompt(
        prompt_type=prompt_type,
        input_tokens=document.tokens,
        example_1=example_document_1,
        example_2=example_document_2,
    )

    model = ChatOpenAI(model=model_name, temperature=temperature)
    parser = PydanticOutputParser(pydantic_object=ModelResponse)

    chain = chat_template | model | parser

    logging.debug(
        f"Evaluated document: {document.name} - Model used: {model.model_name} "
        f"Input length: {len(document.tokens)} - Input tokens: {document.tokens}"
    )

    api_response = chain.invoke({"input": document.tokens})

    logging.debug(f"API response: {api_response}")

    recognized_entities = parse_entities(api_response.data)
    present_entities = document.entities

    example_documents = []
    if prompt_type == "one-shot":
        example_documents.extend([example_document_1.name])
    elif prompt_type == "few-shot":
        example_documents.extend([example_document_1.name, example_document_2.name])

    annotation_result = AnnotationResult(
        document_name=document.name,
        document_length=len(document.tokens),
        prompt_type=prompt_type,
        temperature=temperature,
        examples_documents=example_documents,
        tokens=document.tokens,
        api_response=api_response.data,
        present_entities=present_entities,
        recognized_entities=recognized_entities,
        present_relations=document.relations,
        metrics=calculate_entity_metrics(recognized_entities, present_entities),
    )

    return annotation_result


# TODO: Move to llm package
def generate_prompt(
    prompt_type: str,
    input_tokens: list[str],
    example_1: PetDocument,
    example_2: PetDocument,
) -> ChatPromptTemplate:

    chat_messages = [
        SystemMessage(
            content=(
                "You are an expert in the field of process management. You assist in annotating relevant entities "
                "and relations in natural language process descriptions. You will be provided with definitions of the entities you need to extract."
            )
        )
    ]

    if prompt_type == "zero-shot":
        chat_messages.append(
            HumanMessagePromptTemplate.from_template(zero_shot_template_base).format(
                input=str(input_tokens).replace("'", '"'),
            ),
        )
    elif prompt_type == "one-shot":
        example_annotations_1 = convert_to_template_example(example_1)
        chat_messages.append(
            HumanMessagePromptTemplate.from_template(one_shot_template_base).format(
                input=str(input_tokens).replace("'", '"'),
                example_tokens_1=str(example_1.tokens).replace("'", '"'),
                example_annotations_1=str(example_annotations_1).replace("'", '"'),
            ),
        )
    elif prompt_type == "few-shot":
        example_annotations_1 = convert_to_template_example(example_1)
        example_annotations_2 = convert_to_template_example(example_2)
        chat_messages.append(
            HumanMessagePromptTemplate.from_template(few_shot_template_base).format(
                input=str(input_tokens).replace("'", '"'),
                example_tokens_1=str(example_1.tokens).replace("'", '"'),
                example_annotations_1=str(example_annotations_1).replace("'", '"'),
                example_tokens_2=str(example_2.tokens).replace("'", '"'),
                example_annotations_2=str(example_annotations_2).replace("'", '"'),
            ),
        )

    return ChatPromptTemplate.from_messages(
        chat_messages,
    )
