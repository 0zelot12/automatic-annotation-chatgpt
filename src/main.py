from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

from dotenv import load_dotenv

from templates import actor_template

load_dotenv()

prompt = ChatPromptTemplate.from_template(actor_template)
model = ChatOpenAI()
chain = prompt | model

response = chain.invoke({"input": '["The", "EC", "tells", "the", "INQ", "about", "the", "change", "of", "his", "master", "data", "."]'})

print(response)
