import pytz
from fastapi import APIRouter
from jose import jwt
from datetime import datetime, timedelta
import os

router = APIRouter()

@router.post("/generate-token", summary="Generate JWT Token", description=
            "Generates a valid JWT token for authentication on protected API routes."
            "The token has a configured expiration time and must be used in the "
            "Authorization header as 'Bearer <token>'.")
def generate_token():
    secret = os.getenv("JWT_SECRET", "secret_creditas")
    algorithm = os.getenv("JWT_ALGORITHM", "HS256")

    payload = {
        "sub": "jocimar",
        "role": "admin",
        "exp": datetime.now(pytz.utc) + timedelta(minutes=120)

    }

    token = jwt.encode(payload, secret, algorithm=algorithm)
    return {"token": token}
