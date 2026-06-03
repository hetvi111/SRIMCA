from database import users_collection
from services.hash import hash_password
from datetime import datetime

# Admin user data
admin_data = {
    "name": "Admin",
    "role": "admin",
    "email": "admin@srimca.edu",
    "password": hash_password("admin123"),
    "created_at": datetime.utcnow()
}

# Check if admin exists
existing = users_collection.find_one({"email": admin_data["email"]})
if existing:
    print("Admin already exists!")
else:
    result = users_collection.insert_one(admin_data)
    print(f"Admin added successfully! ID: {result.inserted_id}")
    print("Login: email=admin@srimca.edu, password=admin123")


