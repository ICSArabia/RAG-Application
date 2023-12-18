'''
Test comment added
'''

from flask import Flask
import os
from module1.views import module1_blueprint, module1_namespace
from module2.views import module2_blueprint, module2_namespace
from module3.views import module3_blueprint, module3_namespace
from module4.views import module4_blueprint, module4_namespace
from module5.views import module5_blueprint, module5_namespace

### FE: Reuired Modules ###
from flask import Flask, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS
### FE: Reuired Modules ###

# Import other module blueprints

app = Flask(__name__)

### FE: Allow CORS ###
socketio = SocketIO(app, cors_allowed_origins=["http://localhost", "*:*", "http://icsfinblade.com", "http://54.146.82.200", "http://172.31.55.58:5173", "http://192.168.100.113:5173",  "http://192.168.200.29:5173", "http://46.153.202.111:5173"])
# socketio = SocketIO(app, cors_allowed_origins=["*:*"])
### FE: Allow CORS ###

# Define the upload folder
UPLOAD_FOLDER = r'module5/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Register blueprints
app.register_blueprint(module1_blueprint, url_prefix='/module1')
socketio.on_namespace(module1_namespace)

app.register_blueprint(module2_blueprint, url_prefix='/module2')
socketio.on_namespace(module2_namespace)

app.register_blueprint(module3_blueprint, url_prefix='/module3')
socketio.on_namespace(module1_namespace)

app.register_blueprint(module4_blueprint, url_prefix='/module4')
socketio.on_namespace(module1_namespace)

app.register_blueprint(module5_blueprint, url_prefix='/module5')
socketio.on_namespace(module1_namespace)

# Register other module blueprints

# @app.route("/")
# def index():
#     return "Welcome to the app!"

if __name__ == "__main__":
    # app.run(host="0.0.0.0",port=8080, debug = True) 

    ### FE: Run Sockets ###
    # socketio.run(app, host='192.168.200.29', port=89, debug=False)
    socketio.run(app, host='0.0.0.0', port=8080, debug=True)
    ### FE: Run Sockets ###