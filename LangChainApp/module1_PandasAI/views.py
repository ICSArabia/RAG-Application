from flask import Flask,Blueprint,request,render_template
from LangChainApp.helper import activate_virtualenv
from .pandasai_module import pandas_ai_function

module1_blueprint = Blueprint('module1_blueprint', __name__)

@module1_blueprint.route('/pandasai', methods=['GET', 'POST'])
def module1_index():
    
    structured_retriever = "AAPL10Y"
    question = "Display all column names"
    if request.method == 'POST':
        question = request.form['question']
        
    result, base64_image = pandas_ai_function(question, structured_retriever)

    if result == 'None' and base64_image != 'None':
        result = "Graph Plotted!"

    return render_template('index.html', result=result)


