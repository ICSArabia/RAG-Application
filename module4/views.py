from flask import Blueprint,request,render_template
from flask_socketio import Namespace, emit
from helper import activate_virtualenv

module4_blueprint = Blueprint('module4', __name__)

# @module4_blueprint.route('/', methods=['GET', 'POST'])
class module4_namespace(Namespace):
     def on_submit_question(self, data):
        question = str(data['question'])
        file_name = str(data['docfilename'])
        print(f"this is filename from rag: {file_name}")
        print(question)
                
        output = activate_virtualenv("module4", "test_env4", "rag", question, file_name)
        emit('receive_response', {'response': output})


        # return render_template('index.html', output=output)

module4_blueprint = Blueprint('module4', __name__)
module4_namespace = module4_namespace('/module4')
