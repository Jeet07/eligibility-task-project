#!/usr/bin/env python3
import sys
import os
sys.path.append('/app')

from database import SessionLocal
from models import User, Task
from auth import get_password_hash
from datetime import datetime, timedelta

def seed_data():
    db = SessionLocal()
    
    # Create admin
    admin = db.query(User).filter(User.email == "admin@example.com").first()
    if not admin:
        admin = User(
            email="admin@example.com",
            password=get_password_hash("admin123"),
            role="Admin",
            department="IT",
            experience=10,
            location="Mumbai"
        )
        db.add(admin)
    
    # Create sample users
    users_data = [
        {"email": "john@finance.com", "dept": "Finance", "exp": 6},
        {"email": "jane@finance.com", "dept": "Finance", "exp": 4},
        {"email": "bob@it.com", "dept": "IT", "exp": 5},
    ]
    
    for u in users_data:
        existing = db.query(User).filter(User.email == u["email"]).first()
        if not existing:
            user = User(
                email=u["email"],
                password=get_password_hash("pass123456"),
                department=u["dept"],
                experience=u["exp"],
                location="Mumbai"
            )
            db.add(user)
    
    db.commit()
    print("✅ Seed data added")
    db.close()

if __name__ == "__main__":
    seed_data()
