import sys
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from LangChainApp.module4_RAG.rag_helper import qa_chain_with_memory_and_search, ask_with_memory, break_response_source
from langchain.retrievers import BM25Retriever, EnsembleRetriever
import os
import pickle

# import argparse
# import constants

# os.environ["OPENAI_API_KEY"] = constants.APIKEY

# argparser = argparse.ArgumentParser()
# argparser.add_argument("--query", help="Question to ask")
# argparser.add_argument("--path", help="Path to document", default="")

# args = argparser.parse_args()

# user_query = args.query
# source_file_path = args.path

# CWD = os.getcwd()

# user_query = "Tell me about the 9/11 commission report"
# source_file_path = "module4\documents\FINAL 9-11 Review Commission Report -Unclassified.pdf"

def chat_with_doc(user_query, embedding_file_path, base_retriever_path):
    global llm, qa_chain, memory, search
    global structured_retriever

    temperature = 0.8

    if base_retriever_path is not None:
        with open(base_retriever_path, "rb") as f:
            bm25_retriever = pickle.load(f)  
        bm25_retriever.k = 2
        
        persist_directory = embedding_file_path
        vector_store = Chroma(persist_directory= persist_directory, embedding_function=OpenAIEmbeddings())
        retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k":5})
        
        ensemble_retriever = EnsembleRetriever(retrievers=[bm25_retriever, retriever], weights=[0.2, 0.8])

        llm,qa_chain,memory,search = qa_chain_with_memory_and_search(ensemble_retriever)

        result = ask_with_memory(vector_store, user_query, chat_history=[])

        answer, source = break_response_source(result)
        
    else:
        persist_directory = embedding_file_path
        vector_store = Chroma(persist_directory= persist_directory, embedding_function=OpenAIEmbeddings())
        retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k":5})
        
        llm,qa_chain,memory,search = qa_chain_with_memory_and_search(retriever)

        result = ask_with_memory(vector_store, user_query, chat_history=[])

        answer, source = break_response_source(result)
        
    return answer[0]['answer']
    

# answer = chat_with_doc(user_query, source_file_path)
# print(answer[0]['answer'])