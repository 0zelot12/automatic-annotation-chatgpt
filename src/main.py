import sys
import getopt
import logging
import time

from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import HumanMessagePromptTemplate
from langchain_core.messages import SystemMessage

from datetime import datetime

from entity import Entity, str_to_entity

from dotenv import load_dotenv
from pet_document import PetDocument

from templates import (
    complete_template,
    activity_template,
    activity_data_template,
)

from annotation_result import AnnotationResult
from model_response import ModelResponse
from pet_dataset import PetDataset

from helper import convert_result, convert_tags, write_annotation_results_to_file


# TODO: Move to different location
def annotate_document(
    document: PetDocument, model_name: str, entity_type: Entity
) -> AnnotationResult:
    input_template = complete_template

    # TODO: Refactor
    if entity_type == Entity.ACTIVITY:
        input_template = activity_template

    if entity_type == Entity.ACTIVITY_DATA:
        input_template = activity_data_template

    input_tokens = document.tokens
    reference_annotations = document.ner_tags

    # TODO: Add functionality to annotate multiple entities at once
    chat_template = ChatPromptTemplate.from_messages(
        [
            SystemMessage(
                content=(
                    "You are an expert in the field of process management. You assist in annotating relevant entities "
                    "and relations in natural language process descriptions."
                )
            ),
            HumanMessagePromptTemplate.from_template(input_template).format(
                input=input_tokens
            ),
        ]
    )
    model = ChatOpenAI(model=model_name)
    parser = PydanticOutputParser(pydantic_object=ModelResponse)

    # TODO: Generate input format via parser.get_format_instructions()

    chain = chat_template | model | parser

    logging.debug(
        f"Evaluated document: {document.name} - Model used: {model.model_name} | "
        f"Input length: {len(input_tokens)} - Input tokens: {input_tokens}"
    )

    api_start_time = time.time()
    response = chain.invoke({"input": input_tokens})
    api_end_time = time.time()

    # TODO: Does not work properly
    api_response_time = api_end_time - api_start_time

    logging.debug(f"API response: {response} - Duration: {api_response_time}")

    assert len(input_tokens) == len(
        response.result
    ), "Lengths of input_tokens and response.result do not match"

    converted_response = convert_result(response.result)

    logging.debug(f"Converted response: {converted_response}")

    reference_annotations = convert_tags(reference_annotations)

    annotation_result = AnnotationResult(
        document_name=document.name,
        input_length=len(input_tokens),
        total_number_of_entities=len(reference_annotations),
        response_time=api_response_time,
    )

    # TODO: Implement method to extract all stats at once
    for tag in reference_annotations:
        if tag == Entity.NO_ENTITY.value:
            annotation_result.expected_o += 1
        elif tag == Entity.ACTOR.value:
            annotation_result.expected_actor += 1
        elif tag == Entity.ACTIVITY.value:
            annotation_result.expected_activity += 1
        elif tag == Entity.ACTIVITY_DATA.value:
            annotation_result.expected_activity_data += 1

    for reference, result in zip(reference_annotations, converted_response):
        logging.debug(f"Expected tag: {reference} - Result: {result}")
        if result == reference:
            if result == Entity.ACTOR.value:
                annotation_result.recognized_actor += 1
            elif result == Entity.ACTIVITY.value:
                annotation_result.recognized_activity += 1
            elif result == Entity.ACTIVITY_DATA.value:
                annotation_result.recognized_activity_data += 1
            elif result == Entity.NO_ENTITY.value:
                annotation_result.recognized_o += 1
        else:
            annotation_result.incorrect_entities += 1

    logging.debug(
        f"O recognized: {annotation_result.recognized_o} - Expected: {annotation_result.expected_o} | "
        f"Actor recognized: {annotation_result.recognized_actor} - Expected: {annotation_result.expected_actor} | "
        f"Activity recognized: {annotation_result.recognized_activity} - Expected: {annotation_result.expected_activity} | "
        f"Activity Data recognized: {annotation_result.recognized_activity_data} - Expected: {annotation_result.expected_activity_data} |"
        f"Not recognized correctly: {annotation_result.incorrect_entities} | "
        f"Input length: {annotation_result.input_length}"
    )

    return annotation_result


def main() -> None:
    logging.basicConfig(
        level=logging.DEBUG,
        filename=f"./logs/{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.log",
    )

    load_dotenv()

    # TODO: Evaluate argparse module
    arguments = sys.argv[1:]
    short_options = ""
    long_options = ["document_number=", "model=", "entity_type="]
    options, values = getopt.getopt(arguments, short_options, long_options)

    # Set default values
    document_number = 0
    entity_type = Entity.ACTOR
    model = "gpt-3.5-turbo"

    for o, v in options:
        if o == "--document_number":
            document_number = int(v)
        if o == "--model":
            model = v
        if o == "--entity_type":
            entity_type = str_to_entity(v)

    pet_dataset = PetDataset()
    annotation_results = []

    for i in range(document_number):
        try:
            print(f"Processing document {i}")
            annotation_results.append(
                annotate_document(pet_dataset.get_document(i), model, entity_type)
            )
            print(f"Processing document {i} completed")
        except Exception as e:
            logging.fatal(e)

    if len(annotation_results) > 0:
        write_annotation_results_to_file(annotation_results)


if __name__ == "__main__":
    main()
