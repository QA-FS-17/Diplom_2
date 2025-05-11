# generators.py

import random
import string
import time


def generate_email():
    return f"user{random.randint(1000, 9999)}@example.com"

def generate_password(length=8):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def generate_user_data():
    return {
        "email": generate_email(),
        "password": generate_password(),
        "name": f"User{random.randint(100, 999)}"
    }

def generate_unique_user():
    timestamp = int(time.time())
    return {
        "email": f"user{timestamp}@test.com",
        "password": f"Password{timestamp}",
        "name": f"User{timestamp}"
    }