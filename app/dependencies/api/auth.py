from fastapi import Depends
from fastapi import HTTPException

from fastapi.security import HTTPBearer
from fastapi.security import HTTPAuthorizationCredentials

from sqlalchemy.orm import Session

from app.database import get_db
from app.core.logger import logger
from app.models.user import User
from app.services.auth_service import get_actor_by_token


security = HTTPBearer()


def get_current_actor(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials

    actor = get_actor_by_token(
        db,
        token
    )


    if not actor:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized"
        )
    
    return actor


def require_admin(
    current_actor = Depends(get_current_actor)
):
    if not current_actor.is_admin:
        logger.warning(
            f"ACCESS_DENIED |"
            f"user={current_actor.id}"
        )
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )
    
    return current_actor