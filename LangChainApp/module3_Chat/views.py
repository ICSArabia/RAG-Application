from flask import Blueprint,request,render_template, Response
from LangChainApp.helper import activate_virtualenv
from .chat_with_prompt import chat_with_prompt

module3_blueprint = Blueprint('module3_blueprint', __name__)

@module3_blueprint.route('/chat', methods=['GET', 'POST'])
def module3_index():
    question = "Who are you?"
    if request.method == 'POST':
        question = request.form['question']
        style = 'ICS_Style'
        
    # output = activate_virtualenv("module3", "test_env3", "chat", question, "")
        return Response(chat_with_prompt(question, style), mimetype='text/event-stream')


    return render_template('index.html')