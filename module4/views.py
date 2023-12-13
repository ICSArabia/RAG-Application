from flask import Blueprint,request,render_template
from helper import activate_virtualenv

module4_blueprint = Blueprint('module4', __name__)

@module4_blueprint.route('/', methods=['GET', 'POST'])
def module4_index():
    question = "Summarize the document"
    file_name = r'00-DHP_Vols_I_II_and_III_PB24.pdf'
    if request.method == 'POST':
        question = request.form['question']
        
    output = activate_virtualenv("module4", "test_env4", "rag", question, file_name)


    return render_template('index.html', output=output)