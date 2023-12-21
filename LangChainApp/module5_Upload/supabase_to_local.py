import os 
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

url: str = os.environ.get("SUPABASE_URL") 
key: str = os.environ.get("SUPABASE_ANON_KEY") 
id: str = os.environ.get("SUPABASE_id__hasnain")
email: str = os.environ.get("SUPABASE_EMAIL")
password: str = os.environ.get("SUPABASE_PASSWORD")

supabase: Client = create_client(url, key)

"""
    The frontend will emit an event to the backend when the user uploads a file

    The backend will then update the local dir from the supabase storage

    All the files will be attached to the user's id__hasnain so that if multiple users uploads same file name, 
    it will not be overwritten and will be unique

    The frontend will send the user's id__hasnain with the file name to the backend so that it can retrieve the embeddings of that particular file

"""
# @socketio.on('supabaseListUpdate')
def supabaseListUpdate(id, username):

    # id__hasnain = "4f34ab27-281d-463a-9054-08d4ecda3073"
    # username = "Hasnain"
    ### Here the email and password can be dynamic based on the user that is logged in ###
    # data = supabase.auth.sign_in_with_password({"email": email, "password": password})
    # data = supabase.auth.sign_in_with_password({"email": "mahmed@icsarabia.com", "password": "12345678"})
    data = supabase.auth.sign_in_with_password({"email": email, "password": password})
    resStructured = supabase.storage.from_(id).list('structured')
    resUnstructured = supabase.storage.from_(id).list('unstructured')

    namesStructured = [file['name'] for file in resStructured if file['name'] != '.emptyFolderPlaceholder']
    namesUnstructured = [file['name'] for file in resUnstructured if file['name'] != '.emptyFolderPlaceholder']

    user_structured_path = os.path.join('structured', username)
    user_unstructured_path = os.path.join('unstructured', username)

    if not os.path.exists(user_structured_path):
        os.makedirs(user_structured_path)

    if not os.path.exists(user_unstructured_path):
        os.makedirs(user_unstructured_path)

    localStructured = os.listdir(user_structured_path)
    localUnstructured = os.listdir(user_unstructured_path)

    for file in namesStructured:
        if file not in localStructured:
            download = supabase.storage.from_(id).download(f'structured/{file}')
            with open(f'structured/{username}/{id}-{file}', 'wb') as f:
                f.write(download)

    for file in namesUnstructured:
        if file not in localUnstructured:
            download = supabase.storage.from_(id).download(f'unstructured/{file}')
            with open(f'unstructured/{username}/{id}-{file}', 'wb') as f:
                f.write(download)

    res = supabase.auth.sign_out()
    
# supabaseListUpdate(id, username)
# res = supabase.auth.sign_out()