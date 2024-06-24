from jwt import encode

def create_token(data: dict) -> str:
    token: str = encode(payload=data, key='my_secret_key', algorithm='HS256')
    return token