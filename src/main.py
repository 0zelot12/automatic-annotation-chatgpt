import pandas as pd

from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from dotenv import load_dotenv

from templates import actor_template

load_dotenv()

df = pd.read_parquet("./assets/pet_dataset.parquet")

document_number = 1

prompt = ChatPromptTemplate.from_template(actor_template)
model = ChatOpenAI(model="gpt-3.5-turbo")
# TODO: Use Pydantic parser
parser = StrOutputParser()
chain = prompt | model | parser

print(f"Model used: {model.model_name}")

response = chain.invoke({"input": df["tokens"][document_number]})

# TODO: Implement evaluation of the result

print(response)
