import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Initialize NLTK for Sentiment Analysis
try:
    nltk.download('vader_lexicon', quiet=True)
except:
    pass

sia = SentimentIntensityAnalyzer()

# ================= 1. FAKE REVIEW DETECTION =================
def is_fake_review(text):
    if not text: return True
    words = text.lower().split()

    # Rule 1: Too short (Bot/Spam)
    if len(words) < 4:
        return True

    # Rule 2: High Repetition Ratio (Classic bot spam)
    unique_words = set(words)
    if len(unique_words) / len(words) < 0.4: # e.g. "nice nice nice nice"
        return True

    # Rule 3: Spam Phrases
    spam_triggers = ["best food best", "amazing amazing amazing", "wow wow", "great great"]
    for trigger in spam_triggers:
        if trigger in text.lower():
            return True

    return False

# ================= 2. CLEAN RATING CALCULATION =================
def get_clean_rating(reviews):
    if not reviews:
        return 0

    total = 0
    count = 0

    for r in reviews:
        text = r.get("text", "") or r.get("comment", "")
        rating = r.get("rating", 0)

        if not is_fake_review(text):
            total += rating
            count += 1

    if count == 0:
        return 0

    return round(total / count, 2)

# ================= 3. SMART RECOMMENDATION MODEL =================
def recommend_restaurants():
    """
    TF-IDF based content recommendation.
    """
    # Mock dataset for recommendation
    restaurants = [
        {"name": "Pizza House", "category": "pizza italian cheese"},
        {"name": "Biryani Hub", "category": "biryani spicy indian rice"},
        {"name": "Sweet Shop", "category": "dessert sweets sugar"},
        {"name": "Italian Cafe", "category": "pizza pasta italian"},
        {"name": "Spicy Biryani", "category": "biryani rice spicy"},
        {"name": "Mandi King", "category": "mandi arabic rice meat"},
        {"name": "Dosa Plaza", "category": "south indian dosa tiffins"},
        {"name": "Tandoori Night", "category": "north indian tandoori kebabs"},
        {"name": "Dragon Wok", "category": "chinese noodles manchurian"},
        {"name": "Haleem Palace", "category": "haleem mutton hyderabadi"},
        {"name": "Irani Corner", "category": "irani chai bun maska tiffins"},
        {"name": "Burger Castle", "category": "fast food burger fries"}
    ]

    data = [r["category"] for r in restaurants]
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(data)
    similarity = cosine_similarity(vectors)

    # Assume user interest matches the first entry (Pizza)
    index = 0  
    scores = list(enumerate(similarity[index]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)

    # Return top 3 similar restaurants (excluding itself)
    result = [restaurants[i[0]] for i in scores[1:4]]
    return result

# ================= 4. SENTIMENT ANALYSIS =================
def analyze_sentiment(text):
    scores = sia.polarity_scores(text)
    if scores['compound'] >= 0.05:
        return "Positive"
    elif scores['compound'] <= -0.05:
        return "Negative"
    else:
        return "Neutral"
