from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['restaurant_db']

# Sample Restaurants
restaurants = [
    {
        "restaurant_id": "r1",
        "name": "Hyderabadi Paradise",
        "city": "Hyderabad",
        "cuisine": "Indian",
        "rating": 4.8,
        "address": "Secunderabad, Hyderabad"
    },
    {
        "restaurant_id": "r2",
        "name": "Bawarchi Biryani",
        "city": "Hyderabad",
        "cuisine": "Indian",
        "rating": 4.5,
        "address": "RTC X Roads, Hyderabad"
    }
]

# Sample Cuisines
cuisines = [
    {"city": "Hyderabad", "name": "Hyderabadi Biryani", "type": "Main Course"},
    {"city": "Hyderabad", "name": "Haleem", "type": "Seasonal"}
]

db.restaurants.insert_many(restaurants)
db.cuisines.insert_many(cuisines)

print("Dummy data inserted successfully!")
