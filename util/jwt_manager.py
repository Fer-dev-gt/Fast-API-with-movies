from jwt import encode, decode, DecodeError

def create_token(data: dict) -> str:
    token = encode(payload=data, key="my_secret_key", algorithm="HS256")
    return token

def validate_token(token: str) -> dict:
    try:
        data: dict = decode(token, key="my_secret_key", algorithms=['HS256'])
        return data
    except DecodeError as e:
        raise ValueError("Invalid token format or incorrect key")