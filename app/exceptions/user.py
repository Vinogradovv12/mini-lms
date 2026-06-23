from app.exceptions.base import DomainError


class UserNotFoundError(
    DomainError
):
    code = "user_not_found"

    def __init__(self):
        super().__init__(
            "User not found"
        )


class RoleNotFoundError(
    DomainError
):
    code = "role_not_found"

    def __init__(self):
        super().__init__(
            "Role not found"
        )