from flask import Blueprint, request, jsonify, render_template
from services.google_service import get_nearby_restaurants, get_place_details
from database import db

restaurant_bp = Blueprint('restaurants', __name__)

@restaurant_bp.route('/restaurants/search', methods=['POST'])
def search():
    data = request.get_json()
    lat = data.get('lat')
    lon = data.get('lon')
    keyword = data.get('keyword')
    min_rating = data.get('min_rating', 0)

    results = get_nearby_restaurants(lat, lon, min_rating=min_rating, keyword=keyword)
    return jsonify({"status": "success", "data": results})

@restaurant_bp.route('/restaurants/details/<place_id>', methods=['GET'])
def details(place_id):
    details = get_place_details(place_id)
    if not details:
        return jsonify({"status": "error", "message": "Place not found"}), 404
    
    return jsonify({"status": "success", "data": details})
