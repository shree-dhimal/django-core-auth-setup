import secrets
from django.contrib.auth.hashers import make_password, check_password

def hash_password(raw_password):
    return make_password(raw_password)

def verify_password(raw_password, hashed):
    return check_password(raw_password, hashed)

def generate_token(length=32):
    return secrets.token_hex(length // 2)  # Each byte is represented by two hex digits