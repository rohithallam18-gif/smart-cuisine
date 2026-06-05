from flask import Flask
from flask_cors import CORS
from extensions import mail
from config import Config
from database import db
import os

# 1. Initialize the Flask App
app = Flask(__name__, template_folder='templates', static_folder='static')
app.config.from_object(Config)

# 2. Initialize Extensions
CORS(app)
mail.init_app(app)

# 3. Register Blueprints (from root routes folder)
from routes.auth import auth_bp
from routes.location import location_bp
from routes.restaurants import restaurant_bp
from routes.recommendations import rec_bp
from routes.bookmarks import bookmark_bp
from routes.reviews import review_bp
from routes.main import main_bp

app.register_blueprint(auth_bp)
app.register_blueprint(location_bp)
app.register_blueprint(restaurant_bp)
app.register_blueprint(rec_bp)
app.register_blueprint(bookmark_bp)
app.register_blueprint(review_bp)
app.register_blueprint(main_bp)

if __name__ == "__main__":
    print("Smart Cuisine Backend is running...")
    app.run(debug=True, port=5000)
