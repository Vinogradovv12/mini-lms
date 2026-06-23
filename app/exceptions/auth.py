from app.exceptions.base import DomainError


class InvalidCredentialsError(
    DomainError
):
    code = "invalid_credentials"

    def __init__(self):
        super().__init__(
            "Invalid credentials"
        )


class UserAlreadyExistsError(
    DomainError
):
    code = "user_exists"

    def __init__(self):
        super().__init__(
            "Registration Failed"
        )


class InvalidTokenError(
    DomainError
):
    code = "invalid_token"

    def __init__(self):
        super().__init__(
            "Invalid authentication token"
        )


class AuthenticationRequiredError(
    DomainError
):
    code = "authentication_required"

    def __init__(self):
        super().__init__(
            "Authentication required"
        )


