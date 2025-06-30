from uuid import uuid4

def generate_short_code():
    return uuid4().hex[:6]