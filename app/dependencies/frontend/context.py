from fastapi import Request

from app.authorization.permissions import can_create_course


def base_context(
    request: Request,
    current_user=None,
    **kwargs
):
    return {
        "request": request,
        "current_user": current_user,
        "can_create_course": (
            can_create_course(current_user)
            if current_user
            else False
        ),
        **kwargs
    }