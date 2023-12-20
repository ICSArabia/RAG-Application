'''
Without socket code
'''
from flask import Flask
import os
from module1.views import module1_blueprint
from module2.views import module2_blueprint
from module3.views import module3_blueprint
from module4.views import module4_blueprint
from module5.views import module5_blueprint

# Import other module blueprints

app = Flask(__name__)

# Define the upload folder
UPLOAD_FOLDER = r'module5/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Register blueprints
app.register_blueprint(module1_blueprint, url_prefix='/module1')
app.register_blueprint(module2_blueprint, url_prefix='/module2')
app.register_blueprint(module3_blueprint, url_prefix='/module3')
app.register_blueprint(module4_blueprint, url_prefix='/module4')
app.register_blueprint(module5_blueprint, url_prefix='/module5')

# Register other module blueprints

@app.route("/")
def index():
    return "Welcome to the app!"

if __name__ == "__main__":
    app.run()