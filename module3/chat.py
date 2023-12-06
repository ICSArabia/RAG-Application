from langchain.llms import OpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder 
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
import os
import sys

APIKEY = "***************"
os.environ["OPENAI_API_KEY"] = APIKEY

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
    print(response["text"])
    
    return response["text"]

question = sys.argv[1]
response = chat_with_prompt(question)
print(response)