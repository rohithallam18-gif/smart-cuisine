from flask import Blueprint, request, jsonify
from database import db
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Initialize NLTK
nltk.download('vader_lexicon', quiet=True)
sia = SentimentIntensityAnalyzer()

review_bp = Blueprint('reviews', __name__)

@review_bp.route('/reviews', methods=['POST'])
def add_review():
    data = request.get_json()
    restaurant_id = data.get('restaurant_id')
    user_id = data.get('user_id')
    comment = data.get('comment')
    rating = data.get('rating')

    # Perform Sentiment Analysis
    sentiment_scores = sia.polarity_scores(comment)
    sentiment = "positive" if sentiment_scores['compound'] > 0.05 else "negative" if sentiment_scores['compound'] < -0.05 else "neutral"

    # Use Enhanced Fake Review Detection from ML Models
    from ml_models import is_fake_review
    is_fake = is_fake_review(comment)

    # 1. NEW RULE: Anti-Padding (Max 3 reviews per user per restaurant)
    existing_count = db.reviews.count_documents({
        "user_id": user_id, 
        "restaurant_id": restaurant_id
    })
    
    if existing_count >= 3:
        is_fake = True

    review_doc = {
        "restaurant_id": restaurant_id,
        "user_id": user_id,
        "comment": comment,
        "rating": rating,
        "sentiment": sentiment,
        "is_fake": is_fake,
        "scores": sentiment_scores
    }

    db.reviews.insert_one(review_doc)
    
    # Remove _id for JSON serializability
    review_doc.pop('_id')

    return jsonify({
        "status": "success",
        "analysis": {
            "sentiment": sentiment,
            "is_fake": is_fake
        },
        "data": review_doc
    }), 201

@review_bp.route('/reviews/<restaurant_id>', methods=['GET'])
def get_restaurant_reviews(restaurant_id):
    reviews = list(db.reviews.find({"restaurant_id": restaurant_id}, {"_id": 0}))
    return jsonify({"status": "success", "count": len(reviews), "data": reviews})
