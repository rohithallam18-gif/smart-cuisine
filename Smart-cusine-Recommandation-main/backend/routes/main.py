from flask import Blueprint, render_template, request, jsonify, session, redirect
import sqlite3
import random
from ml_models import is_fake_review, get_clean_rating, recommend_restaurants
from services.google_service import get_nearby_restaurants

main_bp = Blueprint('main', __name__)

@main_bp.route("/")
def login():
    return render_template("login.html")

@main_bp.route("/signup")
def signup():
    return render_template("signup.html")

@main_bp.route("/verify-otp")
def verify_otp_page():
    # Pass type to template (signup or reset)
    otp_type = request.args.get('type', 'signup')
    return render_template("verify_otp.html", type=otp_type)

@main_bp.route("/forgot-password")
def forgot_password():
    return render_template("forgot_password.html")

@main_bp.route("/reset-password")
def reset_password_page():
    return render_template("reset_password.html")

@main_bp.route("/home")
def home():
    lat, lon = 17.3850, 78.4867
    restaurants = get_nearby_restaurants(lat, lon, keyword=session.get("cuisine"))
    ai_picks = recommend_restaurants()
    return render_template("home.html", recs=restaurants, ai_picks=ai_picks)

@main_bp.route("/search")
def search():
    return render_template("dashboard.html")

from database import db # Import MongoDB instance

@main_bp.route("/profile")
def profile():
    email = session.get("email")
    if not email: return redirect("/")
    
    user = db.users.find_one({"email": email})
    return render_template("profile.html", user=user)

@main_bp.route("/settings")
def settings():
    email = session.get("email")
    if not email: return redirect("/")
    user = db.users.find_one({"email": email})
    return render_template("settings.html", user=user)

@main_bp.route("/recommend", methods=["GET", "POST"])
def recommend():
    # Support both POST (form) and GET (query params)
    location = request.values.get("location")
    cuisine = request.values.get("cuisine", "Any")
    lat, lon = request.values.get("lat"), request.values.get("lon")
    
    if lat and lon:
        try:
            lat, lon = float(lat), float(lon)
        except ValueError:
            lat, lon = 17.3850, 78.4867
    else:
        lat, lon = 17.3850, 78.4867 
    
    keyword = request.values.get("keyword")
    search_query = keyword if keyword else (None if cuisine == "Any" else cuisine)
    restaurants = get_nearby_restaurants(lat, lon, keyword=search_query)
    
    return render_template("results.html", location=location, cuisine=cuisine, restaurants=restaurants)

@main_bp.route("/restaurant", strict_slashes=False)
def restaurant_details():
    name = request.args.get("name")
    address = request.args.get("address")
    rating = request.args.get("rating")
    lat = request.args.get("lat")
    lon = request.args.get("lon")
    photo = request.args.get("photo")
    place_id = request.args.get("place_id")
    r = {"name": name, "address": address, "rating": rating, "lat": lat, "lon": lon, "photo": photo, "place_id": place_id}
    return render_template("restaurant.html", r=r)

@main_bp.route("/favorites")
def favorites():
    email = session.get("email")
    if not email: return redirect("/")
    favs = list(db.favorites.find({"user_email": email}, {"_id": 0}))
    return render_template("results.html", location="Favorites", restaurants=favs)

@main_bp.route("/my-reviews")
def my_reviews():
    email = session.get("email")
    if not email: return redirect("/")
    reviews = list(db.reviews.find({}, {"_id": 0}))
    return render_template("my_reviews.html", reviews=reviews)

@main_bp.route("/insights")
def insights():
    return render_template("insights.html")

@main_bp.route("/logout")
def logout():
    session.clear()
    return redirect("/")
@main_bp.route("/api_ai_picks")
def api_ai_picks():
    # 1. Fetch all genuine reviews
    all_reviews = list(db.reviews.find({"is_fake": False}))
    
    # 2. Calculate dynamic rankings
    restaurant_stats = {}
    for rev in all_reviews:
        rid = rev.get("restaurant_id")
        if rid not in restaurant_stats:
            restaurant_stats[rid] = {
                "total": 0, "count": 0, "name": rid,
                "address": "Verified by Community", # Default
                "lat": "17.38", "lon": "78.48" # Hyderabad default
            }
        restaurant_stats[rid]["total"] += rev.get("rating", 0)
        restaurant_stats[rid]["count"] += 1
    
    # 3. Sort by average rating
    top_list = []
    for rid, stats in restaurant_stats.items():
        avg = stats["total"] / stats["count"]
        top_list.append({
            "name": stats["name"],
            "rating": round(avg, 1),
            "address": stats["address"],
            "lat": stats["lat"],
            "lon": stats["lon"],
            "category": "🏆 Most Preferable",
            "is_dynamic": True
        })
    
    top_list = sorted(top_list, key=lambda x: x["rating"], reverse=True)[:5]
    
    # 4. Fallback to AI Mock Data if db is empty
    from ml_models import recommend_restaurants
    mock_picks = recommend_restaurants()
    
    return jsonify({
        "status": "success",
        "top_rated": top_list if top_list else mock_picks,
        "popular": mock_picks # Always show some variety
    })

@main_bp.route("/save_user", methods=["POST"])
def save_user():
    data = request.form
    email = session.get("email")
    if not email: return redirect("/")
    
    user_data = {
        "email": email,
        "first_name": data.get("first_name"),
        "last_name": data.get("last_name"),
        "age": data.get("age"),
        "phone": data.get("phone")
    }
    
    db.users.update_one({"email": email}, {"$set": user_data}, upsert=True)
    
    return redirect("/home")
