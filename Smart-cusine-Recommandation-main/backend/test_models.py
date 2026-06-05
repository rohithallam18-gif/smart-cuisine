import sys
import os

# Add the current directory to sys.path so we can import 'app'
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.ml_models import is_fake_review, get_clean_rating, recommend_restaurants, analyze_sentiment

# Test 1: Fake Review Detection
print("\n--- 🛡️ Testing Fake Review Detection ---")
reviews = [
    {"text": "This place is amazing! Best food ever.", "rating": 5},
    {"text": "good good good", "rating": 1}, 
    {"text": "Bad", "rating": 2}, 
    {"text": "best best best", "rating": 1} 
]

for r in reviews:
    status = "🚨 FAKE" if is_fake_review(r['text']) else "✅ OK"
    print(f"[{status}] Review: '{r['text']}'")

# Test 2: Clean Rating Calculation
print("\n--- ⭐ Testing Clean Rating Calculation ---")
clean_rating = get_clean_rating(reviews)
print(f"Original Avg (inc. fake): 2.25")
print(f"Clean Smart Rating: {clean_rating}")

# Test 3: Sentiment Analysis
print("\n--- 😊 Testing Sentiment Analysis ---")
test_text = "The food was delicious and the service was great!"
sentiment = analyze_sentiment(test_text)
print(f"Text: '{test_text}' -> Sentiment: {sentiment}")

# Test 4: Recommendation Model
print("\n--- 🤖 Testing Smart Recommendations ---")
recs = recommend_restaurants()
print("Top Smart Picks for you:")
for r in recs:
    print(f"- {r['name']} ({r['category']})")
