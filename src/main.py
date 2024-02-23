import sys
import getopt
import logging

from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import HumanMessagePromptTemplate
from langchain_core.messages import SystemMessage

from datetime import datetime

from entity import Entity

from dotenv import load_dotenv
from pet_document import PetDocument

from templates import one_shot_template, few_shot_template, zero_shot_template

from annotation_result import AnnotationResult
from model_response import ModelResponse
from pet_dataset import PetDataset

from helper import (
    process_model_reponse,
    save_annotation_result,
)


# TODO: Move to different location
def annotate_document(document: PetDocument, model_name: str) -> AnnotationResult:
    input_template = zero_shot_template
    input_tokens = document.tokens

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
        f"Evaluated document: {document.name} - Model used: {model.model_name}"
        f"Input length: {len(input_tokens)} - Input tokens: {input_tokens}"
    )

    response = chain.invoke({"input": input_tokens})

    logging.debug(f"API response: {response}")

    processed_response = process_model_reponse(response.data)

    for entity in processed_response:
        print(entity)

    # return annotation_result


def main() -> None:
    logging.basicConfig(
        level=logging.DEBUG,
        filename=f"./logs/{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.log",
    )

    load_dotenv()

    # TODO: Evaluate argparse module
    arguments = sys.argv[1:]
    short_options = ""
    long_options = ["document_number=", "document_name=", "model="]
    options, values = getopt.getopt(arguments, short_options, long_options)

    # Set default values
    document_number = 45
    document_name = None
    model = "gpt-3.5-turbo"

    for o, v in options:
        if o == "--document_number":
            document_number = int(v)
        if o == "--document_name":
            document_name = v
        if o == "--model":
            model = v

    pet_dataset = PetDataset()
    annotation_results = []

    # Temporary solution to able to annotate single documents
    if not document_name:
        for i in range(document_number):
            try:
                document = pet_dataset.get_document(document_number=i)
                print(document.ner_tags)
                # print(f"Processing {document.name}")
                # annotation_result = annotate_document(document, model)
                # annotation_results.append(annotation_result)
                # save_annotation_result(annotation_result)
                # TODO: Evaluate tqdm
                print(f"Processing {document.name} completed")
            except Exception as e:
                print(f"Processing {document.name} failed")
                logging.fatal(e)
    else:
        document = pet_dataset.get_document_by_name(document_name=document_name)
        print(f"Processing {document.name}")
        annotation_result = annotate_document(document, model)
        # annotation_results.append(annotation_result)
        # save_annotation_result(annotation_result)
        print(f"Processing {document.name} completed")
        # try:
        #     document = pet_dataset.get_document_by_name(document_name=document_name)
        #     print(f"Processing {document.name}")
        #     annotation_result = annotate_document(document, model)
        #     # annotation_results.append(annotation_result)
        #     # save_annotation_result(annotation_result)
        #     print(f"Processing {document.name} completed")
        # except Exception as e:
        #     print(f"Processing {document.name} failed")
        #     logging.fatal(e)


if __name__ == "__main__":
    main()
