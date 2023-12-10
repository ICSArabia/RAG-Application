from flask import Blueprint,request,render_template
from helper import activate_virtualenv

module1_blueprint = Blueprint('module1', __name__)

@module1_blueprint.route('/', methods=['GET', 'POST'])
def module1_index():
    
    filename = r"module1\student.csv"
    question = "What is the average marks of the student?"
    if request.method == 'POST':
        question = request.form['question']
        
        
    output = activate_virtualenv("module1", "test_env1", "pandasai_module2", question, filename)


    return render_template('index.html', output=output)
