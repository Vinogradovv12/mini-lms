from fastapi import Depends, HTTPException, Request

from sqlalchemy.orm import Session
from app.core.logger import logger
from app.database import get_db

from app.exceptions.base import RedirectException
from app.exceptions.course import AccessDeniedError
from app.services.auth_service import get_actor_by_token


def get_current_actor_required(
    request: Request,
    db: Session=Depends(get_db)
):
    actor = get_current_actor_optional(
        request,
        db
    )

    if not actor:
        raise RedirectException(
            url="/login",
            status_code=303
        )

    return actor 


def get_current_actor_optional(
    request: Request,
    db: Session
):
    token = request.cookies.get(
        "access_token"
    )

    if not token:
        return None

    try:
        return get_actor_by_token(
            db,
            token
        )
    except Exception:
        return None
    

def require_admin_page(
    actor=Depends(
        get_current_actor_required
    )
):
    if not actor.is_admin:

        logger.warning(
            f"ACCESS_DENIED | "
            f"user={actor.id}"
        )

        raise AccessDeniedError()

    return actor
    
