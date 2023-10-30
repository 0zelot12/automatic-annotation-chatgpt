from langchain.llms import OpenAI

from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from langchain.prompts import PromptTemplate

llm = OpenAI()
chat_model = ChatOpenAI()

template = "You are a process manager. Generate a textual description for the following process: {process}"
prompt = PromptTemplate.from_template(template)

messages = [HumanMessage(content=prompt.format(process="Publish a video game"))]
llm_answer = llm.predict_messages(messages)

print(llm_answer)
