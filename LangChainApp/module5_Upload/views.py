from flask import Blueprint,request,render_template,request, current_app,url_for
import os
from .generate_embeddings import create_and_save_embeddings

module5_blueprint = Blueprint('module5_blueprint', __name__)

def progress_callback(percentage):
    print(f"Progress: {percentage}%")

def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(['txt', 'pdf'])
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@module5_blueprint.route('/upload', methods=['GET','POST'])
def upload():
    if 'file' not in request.files:
        return render_template('upload.html')
    
    file = request.files['file']

    if file.filename == '':
        return 'No selected file'

    if file and allowed_file(file.filename):
        filename = file.filename
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        print('File successfully uploaded')
        create_and_save_embeddings(filename, progress_callback)

    return 'Invalid file type'

