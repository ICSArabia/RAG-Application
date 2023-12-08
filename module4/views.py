from flask import Blueprint,request,render_template
from helper import activate_virtualenv

module4_blueprint = Blueprint('module4', __name__)

@module4_blueprint.route('/', methods=['GET', 'POST'])
def module4_index():
    question = "Tell about the 9/11 commission report"
    file_name = r'D:\ICS_Arabia\ICS_Langchain\module4\documents\FINAL 9-11 Review Commission Report -Unclassified.pdf'
    if request.method == 'POST':
        question = request.form['question']
        
    output = activate_virtualenv("module4", "test_env4", "rag", question, file_name)


    return render_template('index.html', output=output)