from database import users_collection
from werkzeug.security import generate_password_hash
import re

def migrate_passwords():
    users = list(users_collection.find())
    print(f"Checking {len(users)} users for plain text passwords...")
    
    count = 0
    for user in users:
        password = user.get("password")
        if not password:
            continue
            
        # Werkzeug hashes usually follow a pattern like 'method:salt:hash'
        # We can check if it looks like a hash or not.
        # Most common methods start with pbkdf2:, scrypt:, or argon2:
        is_hashed = any(password.startswith(prefix) for prefix in ["pbkdf2:", "scrypt:", "argon2:"])
        
        if not is_hashed:
            print(f"Hashing password for user: {user.get('email')}")
            hashed_password = generate_password_hash(password)
            users_collection.update_one(
                {"_id": user["_id"]},
                {"$set": {"password": hashed_password}}
            )
            count += 1
            
    print(f"Successfully migrated {count} users.")

if __name__ == "__main__":
    migrate_passwords()
