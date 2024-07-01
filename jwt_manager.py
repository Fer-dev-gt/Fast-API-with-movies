from jwt import encode, decode, DecodeError, ExpiredSignatureError, InvalidSignatureError

def create_token(data: dict) -> str:
    token: str = encode(payload=data, key="my_secret_key", algorithm="HS256")
    return token

def validate_token(token: str) -> dict:
    try:
        data = decode(token, key="my_secret_key", algorithms=['HS256'])
        return data
    except DecodeError:
        raise ValueError("Invalid token format or incorrect key")
    except ExpiredSignatureError:
        raise ValueError("Token has expired")
    except InvalidSignatureError:
        raise ValueError("Invalid token signature")
    except Exception as e:
        # Handle other unexpected exceptions
        raise ValueError(f"Token validation failed: {e}")