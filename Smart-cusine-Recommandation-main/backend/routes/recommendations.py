from flask import Blueprint, request, jsonify
from database import db

rec_bp = Blueprint('recommendations', __name__)

@rec_bp.route('/recommendations', methods=['POST'])
def get_recommendations():
    """
    AI-driven recommendation logic.
    """
    data = request.get_json()
    user_id = data.get('user_id')
    
    # 1. Fetch nearby restaurants
    nearby = list(db.restaurants.find({}, {"_id": 0}).limit(10))
    
    # 2. Sort by rating (Simple AI logic)
    sorted_rec = sorted(nearby, key=lambda x: x.get('rating', 0), reverse=True)

    return jsonify({
        "status": "success",
        "user_id": user_id,
        "recommendations": sorted_rec
    })

@rec_bp.route('/cuisines', methods=['GET'])
def get_local_cuisines():
    city = request.args.get('city')
    local_cuisines = list(db.cuisines.find({"city": city}, {"_id": 0}))
    return jsonify({"status": "success", "city": city, "cuisines": local_cuisines})
