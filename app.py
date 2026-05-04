from flask import Flask, render_template
from config import Config
from models import db, Admin
from flask_login import LoginManager
from flask_cors import CORS

# Initialize app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
CORS(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login_page"  # must match function name

# Load user
@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))


# ✅ Frontend routes (UI pages)
@app.route("/")
def home():
    return render_template("admin.html")

@app.route("/login")
def login_page():
    return render_template("admin.html")

@app.route("/dashboard")
def dashboard():
    return render_template("admin.html")


# ✅ Import API routes AFTER app is created
import routes


# Create database tables
with app.app_context():
    db.create_all()


# Run server
if __name__ == "__main__":
    app.run(debug=True)