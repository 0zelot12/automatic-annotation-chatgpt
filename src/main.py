import json
import sys
import getopt
import logging

import pandas as pd

from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from datetime import datetime

from dotenv import load_dotenv

from templates import actor_template


def convert_string_to_list(string_repr):
    # Model adds newlines sometimes
    return json.loads(string_repr.replace("'", '"').replace("\\n", ""))


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


def annotate_document(document_number, model_name):
    load_dotenv()
    df = pd.read_parquet("./assets/pet_dataset.parquet")

    prompt = ChatPromptTemplate.from_template(actor_template)
    model = ChatOpenAI(model=model_name)
    parser = StrOutputParser()  # TODO: Use Pydantic parser

    input_tokens = df["tokens"][document_number]
    document_name = df["document name"][document_number]
    reference_annotations = df["ner_tags"][document_number]

    chain = prompt | model | parser

    logging.info(f"Evaluated document: {document_name}")
    logging.info(f"Model used: {model.model_name}")
    logging.debug(f"Input tokens: {input_tokens}")

    response = chain.invoke({"input": input_tokens})
    logging.debug(f"API response: {response}")

    parsed_response = convert_string_to_list(response)
    logging.debug(f"Parsed response: {parsed_response}")

    converted_response = convert_result(parsed_response, "Actor")
    logging.debug(f"Converted response: {converted_response}")

    assert len(input_tokens) == len(converted_response)

    reference_annotations = convert_tags(reference_annotations, "Actor")

    # TODO: Implement data structure for results
    hit_count_o = 0
    hit_count_actor = 0
    for reference, result in zip(reference_annotations, converted_response):
        logging.debug(f"Expected tag: {reference} - Result: {result}")
        if result == reference:
            if result == "Actor":
                hit_count_actor += 1
            if result == "O":
                hit_count_o += 1

    # TODO: Implement method to extract all stats at once
    total_count_actor = 0
    total_count_o = 0
    for tag in reference_annotations:
        if tag == "O":
            total_count_o += 1
        if tag == "Actor":
            total_count_actor += 1

    logging.debug(f"Hits O: {hit_count_o} - Total: {total_count_o}")
    logging.debug(f"Hits Actor: {hit_count_actor} - Total: {total_count_actor}")
    logging.debug(f"Input length: {len(df['ner_tags'][document_number])}")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        filename=f"./logs/annotation-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.log",
    )
    # TODO: Evaluate argparse module
    arguments = sys.argv[1:]
    short_options = ""
    long_options = ["document_number=", "model="]
    options, values = getopt.getopt(arguments, short_options, long_options)
    document_number = 0
    model = "gpt-3.5-turbo"
    for o, v in options:
        if o == "--document_number":
            document_number = int(v)
        if o == "--model":
            model = v
    annotate_document(document_number, model)
