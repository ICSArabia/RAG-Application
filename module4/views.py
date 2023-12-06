from flask import Blueprint,request,render_template
from helper import activate_virtualenv

module4_blueprint = Blueprint('module4', __name__)

@module4_blueprint.route('/', methods=['GET', 'POST'])
def module3_index():
    question = "What is the average marks of the student?"
    if request.method == 'POST':
        question = request.form['question']
        
    output = activate_virtualenv("module4", "test_env4", "rag", question)


    return render_template('index.html', output=output)