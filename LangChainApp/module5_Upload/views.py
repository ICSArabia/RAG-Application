import os
from flask import Blueprint,request,render_template,request, current_app,url_for,session
from .generate_embeddings import create_and_save_embeddings
from LangChainApp.module5_Upload.supabase_to_local import supabaseListUpdate
from .helper import add_vectorstore

module5_blueprint = Blueprint('module5_blueprint', __name__)

def progress_callback(percentage):
    print(f"Progress: {percentage}%")

def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(['txt', 'pdf'])
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@module5_blueprint.route('/upload', methods=['GET','POST'])
def upload():

    id = "4f34ab27-281d-463a-9054-08d4ecda3073"
    username = "Hasnain"
    un_structured = 'unstructured'
    filename = 'AI-102+Official+Course+Study+Guide'

    supabaseListUpdate(id, username)
    add_vectorstore(username, filename, id)
    return "vectorstore added"
    


