from flask import Flask,Blueprint,request,render_template
from flask_socketio import Namespace, emit
from helper import activate_virtualenv

module2_blueprint = Blueprint('module2', __name__)

class Module1Namespace(Namespace):
# @module2_blueprint.route('/')
    def on_zapier(self, data):
        activate_virtualenv("module2", "test_env2", "langchain_module", "What is the name of the student?")
        # Your logic for Module 1
        return "Module 2 response"

module2_blueprint = Blueprint('module2', __name__)
module2_namespace = Module1Namespace('/module2')