import pandas as pd

from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

from dotenv import load_dotenv

from templates import actor_template

load_dotenv()

df = pd.read_parquet("./assets/pet_dataset.parquet")

document_number = 1

prompt = ChatPromptTemplate.from_template(actor_template)
model = ChatOpenAI()
chain = prompt | model

response = chain.invoke({"input": df["tokens"][document_number]})

# TODO: Use output parser to parse input
# TODO: Implement evaluation of the result

print(response)
