from flask import request, jsonify, render_template
from app import app, db
from models import Admin
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, login_required

# HOME PAGE
@app.route("/")
def home():
    return render_template("admin.html")

# ================= LOGIN =================
@app.route("/api/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        print("DATA RECEIVED:", data)

        email = data.get("email")
        password = data.get("password")

        admin = Admin.query.filter_by(email=email).first()

        if not admin:
            return jsonify({"message": "User not found"}), 404

        if not check_password_hash(admin.password, password):
            return jsonify({"message": "Incorrect password"}), 401

        login_user(admin)

        return jsonify({"message": "Login successful"}), 200

    except Exception as e:
        print("ERROR:", str(e))  # 👈 THIS WILL SHOW REAL ERROR
        return jsonify({"message": "Server error"}), 500


# ================= SIGNUP =================
@app.route("/api/signup", methods=["POST"])
def signup():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    existing = Admin.query.filter_by(email=email).first()
    if existing:
        return jsonify({"message": "User already exists"}), 400

    hashed_password = generate_password_hash(password)

    new_admin = Admin(email=email, password=hashed_password)
    db.session.add(new_admin)
    db.session.commit()

    return jsonify({"message": "User created"}), 201


# ================= LOGOUT =================
@app.route("/api/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out"}), 200