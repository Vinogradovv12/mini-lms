from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.models.role import Role

from app.database import get_db

from app.schemas.role import RoleCreate, RoleResponse

from app.dependencies.api.auth import require_admin
from app.services.role_service import create_role, get_all_roles


router = APIRouter(
    prefix="/api/roles",
    tags=["Roles"]
)

@router.post("/", response_model=RoleResponse)
def create_role_endpoint(
    role: RoleCreate,
    db: Session = Depends(get_db),
    admin=Depends(require_admin)
):
    return create_role(
        db,
        role.name
    )


@router.get("/", response_model=list[RoleResponse])
def get_roles_endpoint(
    db: Session = Depends(get_db),
    admin = Depends(require_admin)
):
    return get_all_roles(
        db
    )