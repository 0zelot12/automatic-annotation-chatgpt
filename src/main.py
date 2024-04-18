import argparse
import os
import logging
import traceback

from datetime import datetime

from dotenv import load_dotenv

from pet.pet_dataset import PetDataset

from utils.visualization import generate_plots

from annotation.annotation import annotate_relations

from server.server import start_server


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
        "--retries",
        required=False,
        default=3,
        help="Number of retries in case an API call fails",
    )

    annotate_parser.add_argument(
        "--matching_mode",
        required=False,
        default="exact",
        help="PLACEHOLDER",
    )

    annotate_parser.add_argument(
        "--training_documents",
        required=False,
        default=["doc-1.1"],
        metavar="string",
        nargs="+",
        help="First document to use as example",
    )

    annotate_parser.add_argument(
        "--temperature",
        required=False,
        default=0.7,
        help="Model temperature",
    )

    # Evaluate
    evaluate_parser = subparsers.add_parser("evaluate", help="evaluate command")
    evaluate_parser.add_argument(
        "--path", required=False, default="./out", help="Path to some directory"
    )

    # Server
    evaluate_parser = subparsers.add_parser("server", help="server command")

    args = parser.parse_args()

    if args.subcommand == "evaluate":
        generate_plots(args.path)
    elif args.subcommand == "server":
        start_server()
    elif args.subcommand == "annotate":
        pet_dataset = PetDataset()
        training_documents = [
            pet_dataset.get_document_by_name(document_name)
            for document_name in args.training_documents
        ]
        if args.document_name:
            document = pet_dataset.get_document_by_name(
                document_name=args.document_name
            )
            for i in range(args.retries):
                print(f"Processing {document.name}")
                try:
                    annotation_result = annotate_relations(
                        document=document,
                        model_name=args.model,
                        training_documents=training_documents,
                        temperature=args.temperature,
                    )
                    annotation_result.save_to_file("./out")
                    print(f"Processing {document.name} completed ✅")
                    break
                except Exception as e:
                    print(f"Processing {document.name} failed ❌")
                    logging.error("An exception occurred: %s", str(e))
                    logging.error(traceback.format_exc())
        else:
            number_of_documents = pet_dataset.get_number_of_documents()
            for i in range(number_of_documents):
                document = pet_dataset.get_document(i)
                for j in range(args.retries):
                    print(f"Processing {document.name}")
                    try:
                        annotation_result = annotate_relations(
                            document=document,
                            model_name=args.model,
                            training_documents=training_documents,
                            temperature=args.temperature,
                        )
                        annotation_result.save_to_file("./out")
                        print(f"Processing {document.name} completed ✅")
                        break
                    except Exception as e:
                        print(f"Processing {document.name} failed ❌")
                        logging.error("An exception occurred: %s", str(e))
                        logging.error(traceback.format_exc())
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
