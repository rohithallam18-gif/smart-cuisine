from flask import Blueprint, request, jsonify, session
from database import users_collection
from services.email_service import generate_otp, send_email_otp
from werkzeug.security import generate_password_hash, check_password_hash
import time
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/get_otp', methods=['POST'])
def get_otp():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email', '').strip().lower()
    name = data.get('name')
    password = data.get('password')

    if not email or not name or not password:
        return jsonify({"status": "error", "message": "Name, email and password are required"}), 400

    # Check if user already exists
    if users_collection.find_one({"email": email}):
        return jsonify({"status": "error", "message": "Email already registered"}), 409

    otp = generate_otp()
    session["signup_data"] = {
        "name": name,
        "email": email,
        "password": password,
        "otp": otp,
        "otp_time": time.time()
    }

    print(f"DEBUG: OTP for {email} is {otp}")
    
    if send_email_otp(email, otp):
        return jsonify({"status": "sent", "message": "OTP sent successfully"})
    else:
        return jsonify({"status": "error", "message": "Failed to send email"}), 500

@auth_bp.route('/verify_otp', methods=['POST'])
def verify_otp():
    data = request.get_json()
    user_otp = data.get('otp')
    signup_data = session.get('signup_data')

    if not signup_data:
        return jsonify({"status": "error", "message": "No registration in progress"}), 400

    if time.time() - signup_data['otp_time'] > 120:
        return jsonify({"status": "error", "message": "OTP expired"}), 400

    if user_otp == signup_data['otp']:
        # Hash the password before saving
        password = signup_data['password']
        hashed_password = generate_password_hash(password)
        
        new_user = {
            "name": signup_data['name'],
            "email": signup_data['email'],
            "password": hashed_password,
            "verified": True,
            "created_at": datetime.utcnow()
        }
        users_collection.insert_one(new_user)
        
        # Clear session signup data
        session.pop('signup_data', None)
        session["email"] = signup_data['email']
        
        return jsonify({"status": "success", "message": "User registered successfully"})
    else:
        return jsonify({"status": "error", "message": "Invalid OTP"}), 401

@auth_bp.route('/login_password', methods=['POST'])
def login_password():
    data = request.get_json()
    email = data.get('email', '').strip().lower()
    password = data.get('password')
    
    if not email or not password:
        return jsonify({"status": "error", "message": "Email and password required"}), 400

    user = users_collection.find_one({"email": email})
    if not user:
        return jsonify({"status": "error", "message": "Email not found. Please sign up first."}), 404
        
    if check_password_hash(user.get("password"), password):
        session["email"] = email
        return jsonify({"status": "success", "message": "Login successful"})
    
    return jsonify({"status": "error", "message": "Incorrect password"}), 401

@auth_bp.route('/forgot_password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    email = data.get('email', '').strip().lower()

    if not email:
        return jsonify({"status": "error", "message": "Email required"}), 400

    user = users_collection.find_one({"email": email})
    if not user:
        return jsonify({"status": "error", "message": "Email not found"}), 404

    otp = generate_otp()
    session["reset_data"] = {
        "email": email,
        "otp": otp,
        "otp_time": time.time(),
        "verified": False
    }

    print(f"DEBUG: Reset OTP for {email} is {otp}")
    
    if send_email_otp(email, otp):
        return jsonify({"status": "sent", "message": "Reset OTP sent successfully"})
    else:
        return jsonify({"status": "error", "message": "Failed to send email"}), 500

@auth_bp.route('/verify_reset_otp', methods=['POST'])
def verify_reset_otp():
    data = request.get_json()
    user_otp = data.get('otp')
    reset_data = session.get('reset_data')

    if not reset_data:
        return jsonify({"status": "error", "message": "No reset in progress"}), 400

    if time.time() - reset_data['otp_time'] > 120:
        return jsonify({"status": "error", "message": "OTP expired"}), 400

    if user_otp == reset_data['otp']:
        reset_data['verified'] = True
        session['reset_data'] = reset_data
        return jsonify({"status": "success", "message": "OTP verified"})
    else:
        return jsonify({"status": "error", "message": "Invalid OTP"}), 401

@auth_bp.route('/reset_password', methods=['POST'])
def reset_password():
    data = request.get_json()
    new_password = data.get('password')
    reset_data = session.get('reset_data')

    if not reset_data or not reset_data.get('verified'):
        return jsonify({"status": "error", "message": "Unauthorized reset attempt"}), 403

    if not new_password or len(new_password) < 6:
        return jsonify({"status": "error", "message": "Password must be at least 6 characters"}), 400

    hashed_password = generate_password_hash(new_password)
    users_collection.update_one(
        {"email": reset_data['email']},
        {"$set": {"password": hashed_password}}
    )
    
    session.pop('reset_data', None)
    return jsonify({"status": "success", "message": "Password reset successfully"})

@auth_bp.route('/profile_check', methods=['GET'])
def profile_check():
    email = session.get("email")
    if not email:
        return jsonify({"status": "new"})
    
    user = users_collection.find_one({"email": email})
    if user and user.get("first_name") and user.get("phone"):
        return jsonify({"status": "existing"})
    return jsonify({"status": "new"})
