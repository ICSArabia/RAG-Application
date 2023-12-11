from flask import Blueprint,request,render_template, Response
from helper import activate_virtualenv
from .chat import chat_response

module3_blueprint = Blueprint('module3', __name__)

@module3_blueprint.route('/', methods=['GET', 'POST'])
def module3_index():
    question = "Who are you?"
    if request.method == 'POST':
        question = request.form['question']
        
    # output = activate_virtualenv("module3", "test_env3", "chat", question, "")
        return Response(chat_response(question), mimetype='text/event-stream')


    return render_template('index.html')