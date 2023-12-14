from flask import Flask,Blueprint,request,render_template
from helper import activate_virtualenv

module1_blueprint = Blueprint('module1', __name__)

@module1_blueprint.route('/', methods=['GET', 'POST'])
def module1_index():
    
    structured_retriever = "AAPL10Y"
    question = "Display all column names"
    if request.method == 'POST':
        question = request.form['question']
        
        
    output = activate_virtualenv("module1", "test_env1", "pandasai_module", question, structured_retriever)
    answer = output.split('\r\n')[0]
    base64_image = output.split('\r\n')[1]

    if answer == 'None' and base64_image != 'None':
        answer = "Graph Plotted!"

    return render_template('index.html', output=output)


