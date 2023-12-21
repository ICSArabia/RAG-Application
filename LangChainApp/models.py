from LangChainApp import db
import uuid

class User(db.Model):
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    chats = db.relationship('Chat', backref='user', lazy=True)

    def __init__(self, username, password):
        self.username = username
        self.password = password
    
class Chat(db.Model):
    
    __tablename__ = 'chat_history'
    
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
    
    id = db.Column(db.Integer, primary_key=True)
    doc_path = db.Column(db.String(200), nullable=False)
    embedding_path = db.Column(db.String(2000), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    def __init__(self, doc_path, embedding_path, user_id):
        self.doc_path = doc_path
        self.embedding_path = embedding_path
        self.user_id = user_id
    