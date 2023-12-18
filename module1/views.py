from flask import Flask,Blueprint,request,render_template
from flask_socketio import Namespace, emit
from helper import activate_virtualenv

module1_blueprint = Blueprint('module1', __name__)

class Module1Namespace(Namespace):
# @module1_blueprint.route('/', methods=['GET', 'POST'])
    def on_submit_question(self, data):
        
        structured_retriever = data['docfilename']
        question = data['question']
        # question = "Display all column names?"
        # structured_retriever = "insurance"
        print(f"this is filename from pandasai: {structured_retriever}")
        print(question)
        output = activate_virtualenv("module1", "test_env1", "pandasai_module", question, structured_retriever)
        # print(output)
        answer = output.split('\r\n')[0]
        base64_image = output.split('\r\n')[1]

        if answer == "None" and base64_image != "None":
            
            answer = "Graph Plotted!"
        # print(f"This is emitting: {output} end")
        print(f"This is answerrrr {answer}")
        print(f"This is base64dddddd {base64_image}")
        emit('receive_response', {'response': answer, 'base64d': base64_image})
      
        # return render_template('index.html', output=output)


module1_blueprint = Blueprint('module1', __name__)
module1_namespace = Module1Namespace('/module1')


