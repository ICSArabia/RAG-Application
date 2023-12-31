def load_document(file):
    import os
    name, extension = os.path.splitext(file)
    # file_path = os.path.join(os.getcwd(), 'module5', 'uploads', file)

    if extension == '.pdf':
        from langchain.document_loaders import PyPDFLoader
        print(f'Loading {file}')
        loader = PyPDFLoader(file)
    elif extension == '.docx':
        from langchain.document_loaders import Docx2txtLoader
        print(f'Loading {file}')
        loader = Docx2txtLoader(file)
    elif extension == '.txt':
        from langchain.document_loaders import TextLoader
        loader = TextLoader(file)
    else:
        print('Document format is not supported!')
        return None

    data = loader.load()
    return data

def chunk_data(data, chunk_size=256):
    from langchain.text_splitter import RecursiveCharacterTextSplitter  
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=0) 
    chunks = text_splitter.split_documents(data) 
    return chunks

def print_embedding_cost(texts):
    import tiktoken
    enc = tiktoken.encoding_for_model('text-embedding-ada-002')
    total_tokens = sum([len(enc.encode(page.page_content)) for page in texts])
    print(f'Total Tokens: {total_tokens}')
    print(f'Embedding Cost in USD: {total_tokens / 1000 * 0.0004:.6f}')
    

def create_embeddings(chunks, file_name):
    from langchain.vectorstores import Chroma
    from langchain.embeddings.openai import OpenAIEmbeddings
    import os

    name, extension = os.path.splitext(file_name)
    # persist_directory = os.path.join(os.getcwd(), 'module5', 'vectorstore_db', f'{file_name}_db')
    persist_directory = f'{name}_db'    
    embeddings = OpenAIEmbeddings()
    vector_store = Chroma.from_documents(chunks, embeddings, persist_directory=persist_directory)
    vector_store.persist()
    return vector_store

def ask_and_get_answer(vector_store, q, k=3):
    from langchain.chains import RetrievalQA
    from langchain.chat_models import ChatOpenAI

    llm = ChatOpenAI(model='gpt-3.5-turbo', temperature=0.2)
    retriever = vector_store.as_retriever(search_type='similarity', search_kwargs={'k': k})
    chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)

    answer = chain.run(q)
    return answer

def ask_with_memory(vector_store, question, chat_history=[]):
    from langchain.chains import ConversationalRetrievalChain
    from langchain.chat_models import ChatOpenAI

    llm = ChatOpenAI(temperature=0.1)
    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k":5})
    crc = ConversationalRetrievalChain.from_llm(llm, retriever)
    result = crc({"question": question, "chat_history": chat_history})
    chat_history.append((question, result["answer"]))
    
    return result, chat_history

def save_retriever(loader,username, filename):
        
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain.retrievers import BM25Retriever
    import pickle
    import os

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

    return chunks

def add_vectorstore(username, filename, id):

    from langchain.document_loaders import PyPDFDirectoryLoader
    from langchain.embeddings import OpenAIEmbeddings
    from langchain.vectorstores import Chroma
    from langchain.document_loaders import PyPDFLoader
    import os
    
    db_path = os.path.join('unstructured',username,f'{username}.db')
    
    if not os.path.exists(db_path):
        
        retriever_dir_path = os.path.join('unstructured',username, 'retriever')
        if not os.path.exists(retriever_dir_path):
            os.mkdir(retriever_dir_path)      
          
        loader = PyPDFDirectoryLoader(f"unstructured/{username}")
        chunks = save_retriever(loader,username, filename)
        persist_directory = os.path.join('unstructured',username,f'{username}.db')
        db = Chroma.from_documents(chunks, OpenAIEmbeddings(), persist_directory=persist_directory)
    
    else:
        persist_directory = os.path.join('unstructured',username,f'{username}.db')
        vector_store = Chroma(persist_directory= persist_directory, embedding_function=OpenAIEmbeddings())
        
        base_directory = os.path.join(os.getcwd(), "unstructured", username)
        target_file = f"{id}-{filename}"  # Target file name without extension

        # Iterate through the directory structure to find the file
        for root, dirs, files in os.walk(base_directory):
            for file in files:
                if file.startswith(target_file) and username in root:
                    file_path = os.path.join(root, file)
                    print(f"Found file at: {file_path}")
                    break
            else:
                continue
            break 
        else:
            print("File not found.")  
        
        loader = PyPDFLoader(file_path)
        chunks = save_retriever(loader,username, filename)
        vector_store.add_documents(chunks)
