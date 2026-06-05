from flask import Blueprint, request, jsonify
import requests

location_bp = Blueprint('location', __name__)

@location_bp.route('/location', methods=['GET'])
def get_location_details():
    lat = request.args.get('lat')
    lon = request.args.get('lon')

    if not lat or not lon:
        return jsonify({"status": "error", "message": "Latitude and Longitude are required"}), 400

    try:
        url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}"
        headers = {'User-Agent': 'IntelligentRestaurantSystem/1.0'}
        response = requests.get(url, headers=headers).json()
        
        address = response.get('address', {})
        
        details = {
            "sublocation": address.get('suburb') or address.get('neighbourhood') or address.get('road'),
            "city": address.get('city') or address.get('town') or address.get('village'),
            "state": address.get('state'),
            "country": address.get('country'),
            "display_name": response.get('display_name')
        }
        
        return jsonify({
            "status": "success", 
            "address": address, # Match frontend expectation
            "details": details
        })
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
