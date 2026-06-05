import requests

GOOGLE_API_KEY = "AIzaSyDAA9513gmfOsnqi6PtnmF2ytGKR90CSkU"

def get_nearby_restaurants(lat, lon, min_rating=0, keyword=None):
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": f"{lat},{lon}",
        "radius": 5000,
        "type": "restaurant",
        "key": GOOGLE_API_KEY
    }
    if keyword:
        params["keyword"] = keyword

    response = requests.get(url, params=params).json()
    restaurants = []

    if response.get("status") != "OK":
        return []

    for place in response.get("results", []):
        rating = place.get("rating", 0)
        if rating >= min_rating:
            photo_url = None
            if "photos" in place:
                ref = place["photos"][0]["photo_reference"]
                photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photo_reference={ref}&key={GOOGLE_API_KEY}"

            restaurants.append({
                "name": place.get("name"),
                "rating": rating,
                "address": place.get("vicinity"),
                "lat": place["geometry"]["location"]["lat"],
                "lon": place["geometry"]["location"]["lng"],
                "photo": photo_url,
                "place_id": place.get("place_id")
            })
    return restaurants

def get_place_details(place_id):
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "place_id": place_id,
        "fields": "reviews,name,rating,vicinity",
        "key": GOOGLE_API_KEY
    }
    res = requests.get(url, params=params).json()
    return res.get("result", {}) if res.get("status") == "OK" else None
