from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv

load_dotenv()

llm = OpenAI()

prompt_template_actor = PromptTemplate(
    input_variables=["country"], template="Whats the captial of {country}?"
)

actor_chain = LLMChain(llm=llm, prompt=prompt_template_actor)

response = actor_chain({"country": "Japan"})

print(response)
