from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

from templates import actor_template

from dotenv import load_dotenv

load_dotenv()

actor_input = [
    "The",
    "EC",
    "tells",
    "the",
    "INQ",
    "about",
    "the",
    "change",
    "of",
    "his",
    "master",
    "data",
    ".",
    "The",
    "INQ",
    "notifies",
    "the",
    "IP",
    "of",
    "the",
    "change",
    ".",
    "The",
    "IP",
    "checks",
    "whether",
    "the",
    "master",
    "data",
    "can",
    "be",
    "changed",
    "at",
    "the",
    "desired",
    "time",
    ".",
    "The",
    "IP",
    "confirmes",
    "the",
    "changes",
    "of",
    "the",
    "INQ",
    "or",
    "the",
    "IP",
    "rejectes",
    "the",
    "changes",
    "of",
    "the",
    "INQ",
    ".",
]


llm = OpenAI()

prompt_template_actor = PromptTemplate(
    input_variables=["input"], template=actor_template
)

actor_chain = LLMChain(llm=llm, prompt=prompt_template_actor)

response = actor_chain({"input": actor_input})

print(response["text"])
