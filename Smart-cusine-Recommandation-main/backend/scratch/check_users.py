from database import users_collection
import json
from bson import json_util

def check_users():
    users = list(users_collection.find().limit(5))
    print(json.dumps(users, default=json_util.default, indent=4))

if __name__ == "__main__":
    check_users()
