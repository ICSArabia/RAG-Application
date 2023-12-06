from flask import Flask
from module1.views import module1_blueprint
from module2.views import module2_blueprint
from module3.views import module3_blueprint
from module4.views import module4_blueprint

# Import other module blueprints

app = Flask(__name__)

# Register blueprints
app.register_blueprint(module1_blueprint, url_prefix='/module1')
app.register_blueprint(module2_blueprint, url_prefix='/module2')
app.register_blueprint(module3_blueprint, url_prefix='/module3')
app.register_blueprint(module4_blueprint, url_prefix='/module4')
# Register other module blueprints

@app.route("/")
def index():
    return "Welcome to the app!"

if __name__ == "__main__":
    app.run()