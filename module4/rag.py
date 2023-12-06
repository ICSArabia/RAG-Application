import sys
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from rag_helper import qa_chain_with_memory_and_search, ask_with_memory, break_response_source
import os

APIKEY = "*****************"
os.environ["OPENAI_API_KEY"] = APIKEY

global llm, qa_chain, memory, search
global structured_retriever

temperature = 0.4

global user_query

# user_query = sys.argv[1]
user_query = 'What is this document about?'
source_file_path = r'C:\llm_project\LLM_Langchain\module4\documents\FINAL 9-11 Review Commission Report -Unclassified.pdf'

persist_directory = source_file_path.split('.')[0] + '_db'
    
vector_store = Chroma(persist_directory= persist_directory, embedding_function=OpenAIEmbeddings())
retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k":5})

llm,qa_chain,memory,search = qa_chain_with_memory_and_search(retriever)

result = ask_with_memory(vector_store, user_query[0], chat_history=[])

answer, source = break_response_source(result)
print('answer:--',answer)