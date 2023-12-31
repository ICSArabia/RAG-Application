import pickle
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from LangChainApp.module4_RAG.rag_helper import qa_chain_with_memory_and_search, ask_with_memory, break_response_source
from langchain.retrievers import BM25Retriever, EnsembleRetriever

def load_retriever(base_retriever_path):
    try:
        with open(base_retriever_path, "rb") as f:
            bm25_retriever = pickle.load(f)
            bm25_retriever.k = 2
            return bm25_retriever
    except FileNotFoundError:
        print("Base retriever file not found.")
        return None
    except Exception as e:
        print(f"Error loading base retriever: {e}")
        return None

def initialize_retriever(embedding_file_path):
    try:
        persist_directory = embedding_file_path
        vector_store = Chroma(persist_directory=persist_directory, embedding_function=OpenAIEmbeddings())
        retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 5})
        return retriever
    except Exception as e:
        print(f"Error initializing retriever: {e}")
        return None

def chat_with_doc(user_query, embedding_file_path, base_retriever_path=None):
    try:
        if base_retriever_path:
            bm25_retriever = load_retriever(base_retriever_path)
            if bm25_retriever:
                vector_store_retriever = initialize_retriever(embedding_file_path)
                if vector_store_retriever:
                    ensemble_retriever = EnsembleRetriever(retrievers=[bm25_retriever, vector_store_retriever], weights=[0.2, 0.8])
                    llm, qa_chain, memory, search = qa_chain_with_memory_and_search(ensemble_retriever)
                    result = ask_with_memory(ensemble_retriever, user_query, chat_history=[])
                    answer, source = break_response_source(result)
        else:
            retriever = initialize_retriever(embedding_file_path)
            if retriever:
                llm, qa_chain, memory, search = qa_chain_with_memory_and_search(retriever)
                result = ask_with_memory(retriever, user_query, chat_history=[])
                answer, source = break_response_source(result)

        return answer[0]['answer'] if answer else None
    except Exception as e:
        print(f"Error in chat_with_doc: {e}")
        return None
