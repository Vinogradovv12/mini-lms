from sqlalchemy.orm import Session

from app.models.role import Role


def create_role(
    db: Session,
    role_name: str
):
    role = Role(
        name=role_name
    )

    db.add(role)

    db.commit()
    
    db.refresh(role)

    return role

def get_all_roles(
    db: Session
):
    return db.query(Role).all()