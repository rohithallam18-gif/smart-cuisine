from flask import Blueprint, request, jsonify, session
from database import db

bookmark_bp = Blueprint('bookmarks', __name__)

@bookmark_bp.route('/save_favorite', methods=['POST'])
def save_favorite():
    email = session.get("email")
    if not email: return jsonify({"status": "error", "message": "Not logged in"}), 401
    
    restaurant = request.get_json()
    restaurant["user_email"] = email
    
    db.favorites.update_one(
        {"user_email": email, "name": restaurant.get("name")},
        {"$set": restaurant},
        upsert=True
    )
    return jsonify({"status": "saved"})

@bookmark_bp.route('/remove_favorite', methods=['POST'])
def remove_favorite():
    email = session.get("email")
    if not email: return jsonify({"status": "error", "message": "Not logged in"}), 401
    
    restaurant = request.get_json()
    db.favorites.delete_one({"user_email": email, "name": restaurant.get("name")})
    return jsonify({"status": "removed"})
