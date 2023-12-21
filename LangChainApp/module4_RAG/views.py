import os
from flask import Blueprint,request,render_template
from LangChainApp.helper import activate_virtualenv
from LangChainApp.module4_RAG.rag import chat_with_doc

module4_blueprint = Blueprint('module4_blueprint', __name__)

@module4_blueprint.route('/RAG', methods=['GET', 'POST'])
def module4_index():

    question = "Summarize the document"
    file_name = r'numpy-user'
    username = "Hasnain"
    id = "4f34ab27-281d-463a-9054-08d4ecda3073"

    embedding_path = os.path.join(os.getcwd(), 'unstructured', username, f'{id}-{file_name}_db' )
    
    if request.method == 'POST':
        question = request.form['question']
        
    # output = activate_virtualenv('module4_RAG', "test_env4", "rag", question, embedding_path)
    output = chat_with_doc(question, embedding_path)


    return render_template('index.html', output=output)