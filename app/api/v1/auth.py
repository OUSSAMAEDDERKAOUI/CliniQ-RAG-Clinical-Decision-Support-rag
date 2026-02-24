from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.user import UserCreate, UserResponse
from app.schemas.auth import Token, LoginRequest
from app.services.auth_service import create_user, authenticate_user
from app.core.security import create_access_token

router = APIRouter()


@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)


@router.post("/login", response_model=Token)
def login(data: LoginRequest, db: Session = Depends(get_db)):

    user = authenticate_user(db, data.username, data.password)

    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token({"sub": user.username})

    return {"access_token": token, "token_type": "bearer"}
