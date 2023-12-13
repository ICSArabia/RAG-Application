import sys
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from rag_helper import qa_chain_with_memory_and_search, ask_with_memory, break_response_source
import os
import argparse
import constants

os.environ["OPENAI_API_KEY"] = constants.APIKEY

argparser = argparse.ArgumentParser()
argparser.add_argument("--query", help="Question to ask")
argparser.add_argument("--path", help="Path to document", default="")

args = argparser.parse_args()

user_query = args.query
source_file_path = args.path

# user_query = "Tell me about the 9/11 commission report"
# source_file_path = "module4\documents\FINAL 9-11 Review Commission Report -Unclassified.pdf"

def chat_with_doc(user_query, source_file_path):
    global llm, qa_chain, memory, search
    global structured_retriever

    temperature = 0.8

    persist_directory = os.path.join('module4', 'documents', source_file_path.split('.')[0] + '_db')
        
    vector_store = Chroma(persist_directory= persist_directory, embedding_function=OpenAIEmbeddings())
    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k":5})

    llm,qa_chain,memory,search = qa_chain_with_memory_and_search(retriever)

    result = ask_with_memory(vector_store, user_query, chat_history=[])

    answer, source = break_response_source(result)
    
    return answer

answer = chat_with_doc(user_query, source_file_path)
print(answer[0]['answer'])