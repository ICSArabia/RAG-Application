import os
from flask import Blueprint,request,render_template
from LangChainApp.helper import activate_virtualenv
from LangChainApp.module4_RAG.rag import chat_with_doc

module4_blueprint = Blueprint('module4_blueprint', __name__)

@module4_blueprint.route('/RAG', methods=['GET', 'POST'])
def module4_index():

    question = "What is the size of the SAN required by the specs?"
    # question = "Summarize numpy user guide and explain some simple functions"
    file_name = r'Scopesplit'
    # file_name = None
    username = "Hasnain"
    id = "4f34ab27-281d-463a-9054-08d4ecda3073"
    
    ###############################################
    
    embedding_path = os.path.join(os.getcwd(), 'unstructured', username, f'{username}.db')
    base_retriever_path = None
    
    if file_name is not None:
        ensemble_retriever = True
        base_retriever_path = os.path.join(os.getcwd(), 'unstructured', username, 'retriever', f'{file_name}_retriever.pkl')
    
    ###############################################

    if request.method == 'POST':
        question = request.form['question']
        
    # output = activate_virtualenv('module4_RAG', "test_env4", "rag", question, embedding_path)
    output = chat_with_doc(question, embedding_path, base_retriever_path)


    return render_template('index.html', output=output)