from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

from templates import actor_template

from dotenv import load_dotenv

load_dotenv()

llm = OpenAI()

prompt_template_actor = PromptTemplate(
    input_variables=["input"], template=actor_template
)

actor_chain = LLMChain(llm=llm, prompt=prompt_template_actor)

# TODO: Read input from file

# response = actor_chain({"input": actor_input})

# print(response["text"])
