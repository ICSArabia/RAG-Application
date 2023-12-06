from flask import Blueprint
from helper import activate_virtualenv

module2_blueprint = Blueprint('module2', __name__)

@module2_blueprint.route('/')
def module2_index():
    activate_virtualenv("module2", "test_env2", "langchain_module", "What is the name of the student?")
    # Your logic for Module 1
    return "Module 2 response"
