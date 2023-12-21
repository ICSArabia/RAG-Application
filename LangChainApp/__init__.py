'''
Without socket code
'''
from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)

# Define the upload folder
UPLOAD_FOLDER = r'D:\ICS_Arabia\ICS_Langchain\LangChainApp\module5_Upload\uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

from LangChainApp.module1_PandasAI.views import module1_blueprint
from LangChainApp.module2_Zapier.views import module2_blueprint
from LangChainApp.module3_Chat.views import module3_blueprint
from LangChainApp.module4_RAG.views import module4_blueprint
from LangChainApp.module5_Upload.views import module5_blueprint
from LangChainApp.users.views import users

# Register blueprints
app.register_blueprint(module1_blueprint)
app.register_blueprint(module2_blueprint)
app.register_blueprint(module3_blueprint)
app.register_blueprint(module4_blueprint)
app.register_blueprint(module5_blueprint)
app.register_blueprint(users)


# Register other module blueprints

@app.route("/")
def index():
    return "Welcome to the app!"
    