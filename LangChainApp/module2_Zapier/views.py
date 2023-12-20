from flask import Blueprint
from LangChainApp.helper import activate_virtualenv

module2_blueprint = Blueprint('module2_blueprint', __name__)

@module2_blueprint.route('/Zapier')
def module2_index():
    activate_virtualenv("module2", "test_env2", "langchain_module", "What is the name of the student?")
    # Your logic for Module 1
    return "Module 2 response"
