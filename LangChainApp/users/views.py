from LangChainApp import app
from flask import request, session,redirect, render_template, url_for
from LangChainApp.models import User, Chat
from LangChainApp import db
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from flask_socketio import SocketIO, join_room, leave_room
import copy

socketio = SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.password == request.form['password']:
            session['username'] = user.username
            return redirect(url_for('chat'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        existing_user = User.query.filter_by(username=request.form['username']).first()
        if existing_user is None:
            new_user = User(username=request.form['username'], password=request.form['password'])
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        else:
            return "User already exists! Try logging in."
    return render_template('register.html')

@app.route('/chat', methods=['GET'])
def chat():
    global session_copy
    
    if 'username' not in session:
        return redirect(url_for('login'))
    user = User.query.filter_by(username=session['username']).first()
    chats = Chat.query.filter_by(user=user).all()

    session_copy = copy.deepcopy(session)

    return render_template('chat.html', chats=chats, username=session['username'])

@socketio.on('message')
def handle_message(data):
    
    user = User.query.filter_by(username=data['username']).first()
    chat = Chat(content=data['message'], user=user)
    
    db.session.add(chat)
    db.session.commit()

    query = data['message']
    llm = ChatOpenAI(model='gpt-3.5-turbo', temperature=0.8)
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    prompt = ChatPromptTemplate.from_template(f"You are ICS Arabia chatbot so answer {query} accordingly.")

    chatbot = LLMChain(llm=llm, prompt=prompt, memory=memory)
    response = chatbot({"query": query})
    response = response['text']
    
    chat = Chat(content=data['message'], response=response, user=user)
    
    db.session.add(chat)
    db.session.commit()
    
    # emit response to appropriate user
    socketio.emit('message', {'user': 'Assistant', 'message': response}, room=request.sid)
    # socketio.emit('message', {'user': 'Assistant', 'message': response})
