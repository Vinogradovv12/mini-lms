from sqlalchemy.orm import Session

from app.core.logger import logger
from app.core.security import create_access_token, hash_password, verify_password, verify_token
from app.exceptions.auth import AuthenticationRequiredError, InvalidCredentialsError, UserAlreadyExistsError
from app.models.role import Role
from app.models.user import User
from app.schemas.auth import TokenResponse


def login_user(
    db: Session,
    email: str,
    password: str
) -> TokenResponse:
    user = (
        db.query(User)
        .filter(
            User.email == email
        )
        .first()
    )

    if not user or not verify_password(
        password,
        user.password_hash
    ):
        logger.warning(
            f"LOGIN_FAILED | "
            f"email={email} | "
        )

        raise InvalidCredentialsError()
    
    logger.info( 
        f"USER_LOGGED_IN | "
        f"email={email}"
    )

    token = create_access_token({
        "sub": str(user.id),
        "role": user.role.name
    })

    return TokenResponse(
        access_token=token,
        token_type="Bearer"
    )


def register_user(
    db: Session,
    username: str,
    email: str,
    password: str
) -> User | None:
    exising_user = (
        db.query(User)
        .filter(
            User.email == email
        )
        .first()
    )

    if exising_user:
        logger.warning(
            f"REGISTER_FAILED | "
            f"email={email}"
        )
        
        raise UserAlreadyExistsError()

    role = (
        db.query(Role)
        .filter(
            Role.name == "student"
        )
        .first()
    )

    user = User(
        username=username,
        email=email,
        password_hash=hash_password(
            password
        ),
        role_id=role.id
    )

    db.add(user)

    db.commit()

    db.refresh(user)

    logger.info(
        f"USER_REGISTERED | "
        f"email={email}"
    )

    return user


def get_actor_by_token(
    db,
    token
):
    payload = verify_token(
        token
    )

    user = (
        db.query(User)
        .filter(
            User.id == int(
                payload["sub"]
            )
        )
        .first()
    )

    if not user:
        raise AuthenticationRequiredError()

    return user