from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt

from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.config import settings
from app.models.user import User

def get_current_user(
    token: str,
    db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        username = payload.get("sub")

        if username is None:
            raise HTTPException(status_code=401)

    except JWTError:
        raise HTTPException(status_code=401)

    user = db.query(User).filter(User.username == username).first()

    if user is None:
        raise HTTPException(status_code=401)

    return user
