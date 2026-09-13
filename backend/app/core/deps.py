from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import decode_access_token
from app.database.database import get_db
from app.database.models import User

bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    """
    Require a valid Bearer token and return the corresponding User.
    Raises 401 if missing/invalid/expired, or if the user no longer exists.
    """
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated. Please log in.",
        )

    email = decode_access_token(credentials.credentials)

    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Your session has expired. Please log in again.",
        )

    user = db.query(User).filter(User.email == email).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Account not found. Please log in again.",
        )

    return user


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    """
    Gate an endpoint to the single account configured as ADMIN_EMAIL.
    MLForge has no broader role system yet - this exists specifically for
    the analytics dashboard, which shouldn't be visible to every user.
    """
    if not settings.ADMIN_EMAIL or current_user.email != settings.ADMIN_EMAIL:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this.",
        )
    return current_user