import logging

from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import HumanMessagePromptTemplate
from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI

from pet.pet_document import PetDocument

from llm.templates import (
    zero_shot_template_base,
    one_shot_template_base,
    few_shot_template_base,
    relation_template,
)

from llm.utils import generate_model_relations

from annotation.annotation_result import AnnotationResult
from llm.model_response import ModelResponse

from utils.helper import (
    parse_entities,
    calculate_metrics,
    convert_to_template_example,
)


def annotate_relations(
    document: PetDocument,
    example_document: PetDocument,
    model_name: str,
    prompt_type: str,
    temperature: float,
) -> None:
    chat_messages = [
        SystemMessage(
            content=(
                "You are an expert in the field of process management. You assist in annotating relevant entities "
                "and relations in natural language process descriptions. You will be provided with definitions of the entities you need to extract."
            )
        )
    ]

    test_relations = generate_model_relations(document.relations)
    training_relations = generate_model_relations(example_document.relations)

    chat_messages.append(
        HumanMessagePromptTemplate.from_template(relation_template).format(
            example_input=training_relations,
            input=test_relations,
        ),
    )

    template = ChatPromptTemplate.from_messages(
        chat_messages,
    )

    model = ChatOpenAI(model=model_name, temperature=temperature)
    chain = template | model

    # Why do I need input here?
    api_response = chain.invoke({"input": ""})

    print(api_response.content)

    return None


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
        metrics=calculate_metrics(recognized_entities, present_entities),
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
