import os
from flask import Blueprint,request,render_template,request, current_app,url_for,session
from .generate_embeddings import create_and_save_embeddings
from LangChainApp.module5_Upload.supabase_to_local import supabaseListUpdate

module5_blueprint = Blueprint('module5_blueprint', __name__)

def progress_callback(percentage):
    print(f"Progress: {percentage}%")

def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(['txt', 'pdf'])
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@module5_blueprint.route('/upload', methods=['GET','POST'])
def upload():

    id = "4f34ab27-281d-463a-9054-08d4ecda3073"
    username = "Hasnain"
    un_structured = 'unstructured'
    filename = 'Scopesplit'

    supabaseListUpdate(id, username)
    
    #############################################################
    
    from langchain.document_loaders import PyPDFDirectoryLoader
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from dotenv import load_dotenv
    from langchain.embeddings import OpenAIEmbeddings
    from langchain.vectorstores import Chroma
    from langchain.retrievers import BM25Retriever, EnsembleRetriever
    from langchain.document_loaders import PyPDFLoader
    import pickle
    
    # check if any database embedding is already generated
    
    db_path = os.path.join('unstructured',username,f'{username}.db')
    
    if not os.path.exists(db_path):
        
        retriever_dir_path = os.path.join('unstructured',username, 'retriever')
        if not os.path.exists(retriever_dir_path):
            os.mkdir(retriever_dir_path)      
          
        loader = PyPDFDirectoryLoader(f"unstructured/{username}")
        docs = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(
            # Set a really small chunk size, just to show.
            chunk_size = 256,
            chunk_overlap  = 0,
            length_function = len,
            is_separator_regex = False,
        )

        chunks = text_splitter.split_documents(docs)

        bm25_retriever = BM25Retriever.from_documents(chunks)

        retriever_path = os.path.join('unstructured',username,'retriever',f'{filename}_retriever.pkl')
        with open(retriever_path, "wb") as f:
            pickle.dump(bm25_retriever, f) 

        embeddings_model = OpenAIEmbeddings()
        persist_directory = os.path.join('unstructured',username,f'{username}.db')
        db = Chroma.from_documents(chunks, OpenAIEmbeddings(), persist_directory=persist_directory)
    
    else:
        persist_directory = os.path.join('unstructured',username,f'{username}.db')
        vector_store = Chroma(persist_directory= persist_directory, embedding_function=OpenAIEmbeddings())
        
        base_directory = r'D:\ICS_Arabia\ICS_Langchain\unstructured'
        target_file = f"{id}-{filename}"  # Target file name without extension

        # Iterate through the directory structure to find the file
        for root, dirs, files in os.walk(base_directory):
            for file in files:
                if file.startswith(target_file) and username in root:
                    file_path = os.path.join(root, file)
                    print(f"Found file at: {file_path}")
                    break
            else:
                continue  # Continue to the next iteration if not found
            break  # Break the outer loop if file is found
        else:
            print("File not found.")  
        
        loader = PyPDFLoader(file_path)

        docs = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(
            # Set a really small chunk size, just to show.
            chunk_size = 256,
            chunk_overlap  = 0,
            length_function = len,
            is_separator_regex = False,
        )

        chunks = text_splitter.split_documents(docs) 
        
        bm25_retriever = BM25Retriever.from_documents(chunks)

        retriever_path = os.path.join('unstructured',username,'retriever',f'{filename}_retriever.pkl')
        with open(retriever_path, "wb") as f:
            pickle.dump(bm25_retriever, f) 

        embeddings_model = OpenAIEmbeddings()

        vector_store.add_documents(chunks)
        
    #############################################################

    # if un_structured == 'unstructured':
    #     base_directory = r'D:\ICS_Arabia\ICS_Langchain_Development\unstructured'
    #     target_file = f"{id}-{filename}"  # Target file name without extension

    #     # Iterate through the directory structure to find the file
    #     for root, dirs, files in os.walk(base_directory):
    #         for file in files:
    #             if file.startswith(target_file) and username in root:
    #                 file_path = os.path.join(root, file)
    #                 print(f"Found file at: {file_path}")
    #                 break
    #         else:
    #             continue  # Continue to the next iteration if not found
    #         break  # Break the outer loop if file is found
    #     else:
    #         print("File not found.")  
            
        
    #     create_and_save_embeddings(file_path, progress_callback)
    #     return "Embeddings generated successfully"

