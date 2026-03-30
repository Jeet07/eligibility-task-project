from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database import get_db
from models import User
from config import config

SECRET_KEY = config.SECRET_KEY
ALGORITHM = config.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = config.ACCESS_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(
    schemes=["argon2", "bcrypt"],
    deprecated="auto"
)

security = HTTPBearer()

# ---------------- PASSWORD ---------------- #
def get_password_hash(password: str):
    if len(password) < 8:
        raise HTTPException(status_code=400, detail="Password too short")
    
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

# ---------------- TOKEN ---------------- #
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow()
    })
    
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# ---------------- USER ---------------- #
def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    if not token or not token.credentials:
        raise HTTPException(status_code=401, detail="Missing token")

    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        role = payload.get("role")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = db.query(User).filter(User.id == int(user_id)).first()

        if user is None:
            raise HTTPException(status_code=401, detail="User not found")

        return user

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def check_admin(user: User = Depends(get_current_user)):
    if user.role != "Admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return user
