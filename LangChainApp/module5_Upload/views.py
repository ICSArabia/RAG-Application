import os
from flask import Blueprint,request,render_template,request, current_app,url_for,session
from .generate_embeddings import create_and_save_embeddings
from LangChainApp.module5_Upload.supabase_to_local import supabaseListUpdate

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
    filename = 'numpy-user'

    supabaseListUpdate(id, username)

    if un_structured == 'unstructured':
        base_directory = r'D:\ICS_Arabia\ICS_Langchain_Development\unstructured'
        target_file = f"{id}-{filename}"  # Target file name without extension

        # Iterate through the directory structure to find the file
        for root, dirs, files in os.walk(base_directory):
            for file in files:
                if file.startswith(target_file) and username in root:
                    file_path = os.path.join(root, file)
                    print(f"Found file at: {file_path}")
                    break
            else:
                continue  # Continue to the next iteration if not found
            break  # Break the outer loop if file is found
        else:
            print("File not found.")  
            
        
        create_and_save_embeddings(file_path, progress_callback)
        return "Embeddings generated successfully"

