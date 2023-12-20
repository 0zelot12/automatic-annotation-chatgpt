import json
import sys
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
    return json.loads(string_repr.replace("'", "\"").replace("\\n", ""))

def annotate_document(document_number):
    load_dotenv()
    df = pd.read_parquet("./assets/pet_dataset.parquet")

    prompt = ChatPromptTemplate.from_template(actor_template)
    model = ChatOpenAI(model="gpt-3.5-turbo")
    parser = StrOutputParser() # TODO: Use Pydantic parser

    input_tokens = df["tokens"][document_number]
    document_name = df['document name'][document_number]

    chain = prompt | model | parser

    logging.info(f"Evaluated document: {document_name}")
    logging.info(f"Model used: {model.model_name}")
    logging.debug(f"Input tokens: {input_tokens}")

    response = chain.invoke({"input": input_tokens})

    logging.debug(f"API response: {response}")

    response = convert_string_to_list(response)

    logging.debug(f"Parsed response: {response}")

    # TODO: Implement evaluation of the result

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG, 
        filename=f"./logs/annotation-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.log"
    )
    document_number = int(sys.argv[1])
    annotate_document(document_number)
