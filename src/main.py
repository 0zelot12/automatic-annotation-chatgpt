import json
import sys
import getopt
import logging

import pandas as pd

from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser

from datetime import datetime

from dotenv import load_dotenv

from templates import actor_template, activity_template, activity_data_template
from annotation_result import AnnotationResult
from model_response import ModelResponse


def convert_tags(tags, entity):
    filtered_tags = []
    for tag in tags:
        if tag == f"B-{entity}" or tag == f"I-{entity}":
            filtered_tags.append(entity)
        else:
            filtered_tags.append("O")
    return filtered_tags


def convert_result(annotations, entity):
    converted_results = []
    for annotation in annotations:
        if annotation.startswith("<A>"):
            converted_results.append(entity)
        else:
            converted_results.append("O")
    return converted_results


def get_entity_type_count(tags, entity):
    count = 0
    for tag in tags:
        if tag == f"B-{entity}" or tag == f"I-{entity}":
            count += 1
    return count


def annotate_document(document_number, model_name, entity_type):
    load_dotenv()
    df = pd.read_parquet("./assets/pet_dataset.parquet")

    input_template = actor_template

    if entity_type == "Activity":
        input_template = activity_template

    if entity_type == "Actibity Data":
        input_template = activity_data_template

    prompt = ChatPromptTemplate.from_template(input_template)
    model = ChatOpenAI(model=model_name)
    parser = PydanticOutputParser(pydantic_object=ModelResponse)

    # TODO: Generate input format via parser.get_format_instructions()

    input_tokens = df["tokens"][document_number].tolist()
    document_name = df["document name"][document_number]
    reference_annotations = df["ner_tags"][document_number]

    chain = prompt | model | parser

    logging.info(f"Evaluated document: {document_name}")
    logging.info(f"Model used: {model.model_name}")
    logging.debug(f"Input tokens: {input_tokens}")
    logging.debug(f"Input length: {input_tokens}")

    response = chain.invoke({"input": input_tokens})
    logging.debug(f"API response: {response}")

    assert len(input_tokens) == len(response.result)

    converted_response = convert_result(response.result, entity_type)
    logging.debug(f"Converted response: {converted_response}")

    reference_annotations = convert_tags(reference_annotations, entity_type)

    annotation_result = AnnotationResult(input_length=len(input_tokens))

    for reference, result in zip(reference_annotations, converted_response):
        logging.debug(f"Expected tag: {reference} - Result: {result}")
        if result == reference:
            if result == "Actor":
                annotation_result.recognized_actor += 1
            if result == "Activity":
                annotation_result.recognized_activity += 1
            if result == "Activity Data":
                annotation_result.recognized_activity_data += 1
            if result == "O":
                annotation_result.recognized_o += 1

    # TODO: Implement method to extract all stats at once
    for tag in reference_annotations:
        if tag == "O":
            annotation_result.expected_o += 1
        if tag == "Actor":
            annotation_result.expected_actor += 1
        if tag == "Actitvity":
            annotation_result.expected_activity += 1
        if tag == "Actitvity Data":
            annotation_result.expected_activity_data += 1

    logging.debug(
        f"O recognized: {annotation_result.recognized_o} - Expected: {annotation_result.recognized_o}"
    )

    logging.debug(
        f"Actor recognized: {annotation_result.recognized_actor} - Expected: {annotation_result.expected_actor}"
    )

    logging.debug(
        f"Activity recognized: {annotation_result.recognized_activity} - Expected: {annotation_result.expected_activity}"
    )

    logging.debug(
        f"Activity Data recognized: {annotation_result.recognized_activity_data} - Expected: {annotation_result.expected_activity_data}"
    )

    logging.debug(f"Input length: {annotation_result.input_length}")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        filename=f"./logs/annotation-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.log",
    )
    # TODO: Evaluate argparse module
    arguments = sys.argv[1:]
    short_options = ""
    long_options = ["document_number=", "model=", "entity_type="]
    options, values = getopt.getopt(arguments, short_options, long_options)
    document_number = 0
    entity_type = "Actor"
    model = "gpt-3.5-turbo"
    for o, v in options:
        if o == "--document_number":
            document_number = int(v)
        if o == "--model":
            model = v
        if o == "--entity_type":
            entity_type = v
    annotate_document(document_number, model, entity_type)
