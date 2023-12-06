from flask import Blueprint,request,render_template
from helper import activate_virtualenv

module3_blueprint = Blueprint('module3', __name__)

@module3_blueprint.route('/', methods=['GET', 'POST'])
def module3_index():
    question = "What is the average marks of the student?"
    if request.method == 'POST':
        question = request.form['question']
        
    output = activate_virtualenv("module3", "test_env3", "chat", question)


    return render_template('index.html', output=output)