from langchain.llms import OpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder 
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
import os
import argparse

APIKEY = "******************"
os.environ["OPENAI_API_KEY"] = APIKEY

argparser = argparse.ArgumentParser()
argparser.add_argument("--query", help="Question to ask")
argparser.add_argument("--path", help="Path to document", default="")

args = argparser.parse_args()

def chat_with_prompt(user_query):
    # LLM 
    llm = ChatOpenAI(model='gpt-4-0613', temperature=0.4)

    # Prompt
    prompt = ChatPromptTemplate.from_template("You are ICS Arabia chatbot so answer {query} accordingly")

    # Memory
    memory = ConversationBufferMemory(
        memory_key="chat_history", 
        return_messages=True
    )

    # Chain
    chatbot = LLMChain(
        llm=llm,
        prompt=prompt,
        memory=memory
    )

    # Usage
    response = chatbot({
        "query": user_query  
    })
    
    return response["text"]

question = args.query
response = chat_with_prompt(question)
print(response)