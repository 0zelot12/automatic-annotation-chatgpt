import sys
import argparse
import os
import logging
import traceback

from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import HumanMessagePromptTemplate
from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI

from datetime import datetime

from dotenv import load_dotenv
from pet_document import PetDocument

from templates import zero_shot_template, one_shot_template, few_shot_template

from annotation_result import AnnotationResult
from model_response import ModelResponse
from pet_dataset import PetDataset

from helper import (
    parse_entities,
    calculate_metrics,
    convert_to_template_example,
    evaluate_results,
)


def main() -> None:
    logging.basicConfig(
        level=logging.DEBUG,
        filename=f"./logs/{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.log",
    )

    load_dotenv()

    if "OPENAI_API_KEY" not in os.environ:
        print(
            "OPENAI_API_KEY was not detected. Please create a .env file and add the key."
        )
        return

    parser = argparse.ArgumentParser(description="Automatic Annotation ChatGPT")
    subparsers = parser.add_subparsers(title="subcommands", dest="subcommand")

    # Annotate
    annotate_parser = subparsers.add_parser("annotate", help="annotate command")
    annotate_parser.add_argument(
        "--document_name", required=False, help="Name of the document to annotate"
    )
    annotate_parser.add_argument(
        "--model", required=False, default="gpt-3.5-turbo", help="OpenAI model to use"
    )
    annotate_parser.add_argument(
        "--prompt_type", required=False, default="one-shot", help="Prompt type"
    )
    annotate_parser.add_argument(
        "--retries",
        required=False,
        default=3,
        help="Number of retries in case an API call fails",
    )
    annotate_parser.add_argument(
        "--example_document_1",
        required=False,
        default="doc-1.1",
        help="First document to use as example",
    )
    annotate_parser.add_argument(
        "--example_document_2",
        required=False,
        default="doc-3.1",
        help="Second document to use as example",
    )

    # Evaluate
    evaluate_parser = subparsers.add_parser("evaluate", help="evaluate command")
    evaluate_parser.add_argument(
        "--path", required=False, default="./out", help="Path to some directory"
    )

    args = parser.parse_args()

    if args.subcommand == "evaluate":
        evaluate_results(args.path)
    elif args.subcommand == "annotate":
        pet_dataset = PetDataset()
        example_document_1 = pet_dataset.get_document_by_name(
            document_name=args.example_document_1
        )
        example_document_2 = pet_dataset.get_document_by_name(
            document_name=args.example_document_2
        )
        if args.document_name:
            document = pet_dataset.get_document_by_name(
                document_name=args.document_name
            )
            for i in range(args.retries):
                print(f"Processing {document.name}")
                try:
                    annotation_result = annotate_document(
                        document=document,
                        model_name=args.model,
                        example_document_1=example_document_1,
                        example_document_2=example_document_2,
                        prompt_type=args.prompt_type,
                    )
                    annotation_result.save_to_file("./out")
                    print(f"Processing {document.name} completed")
                    break
                except Exception as e:
                    print(f"Processing {document.name} failed")
                    logging.error("An exception occurred: %s", str(e))
                    logging.error(traceback.format_exc())
        else:
            number_of_documents = len(pet_dataset.get_data())
            for i in range(number_of_documents):
                document = pet_dataset.get_document(i)
                for j in range(args.retries):
                    print(f"Processing {document.name}")
                    try:
                        annotation_result = annotate_document(
                            document=document,
                            model_name=args.model,
                            example_document_1=example_document_1,
                            example_document_2=example_document_2,
                            prompt_type=args.prompt_type,
                        )
                        annotation_result.save_to_file("./out")
                        print(f"Processing {document.name} completed")
                        break
                    except Exception as e:
                        print(f"Processing {document.name} failed")
                        logging.error("An exception occurred: %s", str(e))
                        logging.error(traceback.format_exc())
    else:
        parser.print_help()


# TODO: Move to different location
def annotate_document(
    document: PetDocument,
    example_document_1: PetDocument,
    example_document_2: PetDocument,
    model_name: str,
    prompt_type: str,
) -> AnnotationResult:

    chat_template = generate_prompt(
        prompt_type=prompt_type,
        input_tokens=document.tokens,
        example_1=example_document_1,
        example_2=example_document_2,
    )

    model = ChatOpenAI(model=model_name)
    parser = PydanticOutputParser(pydantic_object=ModelResponse)

    # TODO: Generate input format via parser.get_format_instructions()

    chain = chat_template | model | parser

    logging.debug(
        f"Evaluated document: {document.name} - Model used: {model.model_name} "
        f"Input length: {len(document.tokens)} - Input tokens: {document.tokens}"
    )

    api_response = chain.invoke({"input": document.tokens})

    logging.debug(f"API response: {api_response}")

    recognized_entities = parse_entities(api_response.data)
    present_entities = document.get_entities()

    example_documents = []
    if prompt_type == "one-shot":
        example_documents.append(example_document_1.name)
    elif prompt_type == "few-shot":
        example_documents.append(example_document_1.name, example_document_2.name)

    annotation_result = AnnotationResult(
        document_name=document.name,
        document_length=len(document.tokens),
        prompt_type=prompt_type,
        examples_documents=example_documents,
        tokens=document.tokens,
        api_response=api_response.data,
        present_entities=present_entities,
        recognized_entities=recognized_entities,
        metrics=calculate_metrics(recognized_entities, present_entities),
    )

    return annotation_result


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
            HumanMessagePromptTemplate.from_template(zero_shot_template).format(
                input=str(input_tokens).replace("'", '"'),
            ),
        )
    elif prompt_type == "one-shot":
        example_annotations_1 = convert_to_template_example(example_1)
        chat_messages.append(
            HumanMessagePromptTemplate.from_template(one_shot_template).format(
                input=str(input_tokens).replace("'", '"'),
                example_tokens_1=str(example_1.tokens).replace("'", '"'),
                example_annotations_1=str(example_annotations_1).replace("'", '"'),
            ),
        )
    elif prompt_type == "few-shot":
        example_annotations_1 = convert_to_template_example(example_1)
        example_annotations_2 = convert_to_template_example(example_2)
        chat_messages.append(
            HumanMessagePromptTemplate.from_template(few_shot_template).format(
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


if __name__ == "__main__":
    main()
