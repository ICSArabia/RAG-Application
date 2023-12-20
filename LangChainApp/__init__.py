'''
Without socket code
'''
from flask import Flask
import os
from LangChainApp.module1_PandasAI.views import module1_blueprint
from LangChainApp.module2_Zapier.views import module2_blueprint
from LangChainApp.module3_Chat.views import module3_blueprint
from LangChainApp.module4_RAG.views import module4_blueprint
from LangChainApp.module5_Upload.views import module5_blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)

# Define the upload folder
UPLOAD_FOLDER = r'D:\ICS_Arabia\ICS_Langchain\LangChainApp\module5_Upload\uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Register blueprints
app.register_blueprint(module1_blueprint)
app.register_blueprint(module2_blueprint)
app.register_blueprint(module3_blueprint)
app.register_blueprint(module4_blueprint)
app.register_blueprint(module5_blueprint)

# Register other module blueprints

@app.route("/")
def index():
    return "Welcome to the app!"

################################

class User(db.Model):
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    chats = db.relationship('Chat', backref='users', lazy=True)
    RAGs = db.relationship('RAG', backref='users', lazy=True)
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
    
class Chat(db.Model):
    
    __tablename__ = 'chat_history'
    
    users = db.relationship(User)
    
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    def __init__(self, question, response, user_id):
        self.question = question
        self.response = response
        self.user_id = user_id

class RAG(db.Model):
    
    __tablename__ = 'RAG_Document'
    
    users = db.relationship(User)
    
    id = db.Column(db.Integer, primary_key=True)
    doc_path = db.Column(db.String(200), nullable=False)
    embedding_path = db.Column(db.String(2000), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    def __init__(self, doc_path, embedding_path, user_id):
        self.doc_path = doc_path
        self.embedding_path = embedding_path
        self.user_id = user_id
    