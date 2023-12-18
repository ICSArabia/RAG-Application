from flask import Blueprint,request,render_template, Response
from flask_socketio import Namespace, emit
from helper import activate_virtualenv
from .chat_with_prompt import chat_with_prompt

module3_blueprint = Blueprint('module3', __name__)

# @module3_blueprint.route('/', methods=['GET', 'POST'])
class Module3Namespace(Namespace):
    def on_chatgpt_question(self, data):
        question = data['question']
        print(question)
        style = data['stylevar']
        if style == "None":
            style = None
        response = chat_with_prompt(question, style)
        # print(response)
        emit('chat_response', {'answer': response})
        
    # output = activate_virtualenv("module3", "test_env3", "chat", question, "")
        return Response(chat_with_prompt(question, style), mimetype='text/event-stream')


    # return render_template('index.html')

module3_blueprint = Blueprint('module3', __name__)
module3_namespace = Module3Namespace('/module3')