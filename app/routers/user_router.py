from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.deps import get_db
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import UserService
from app.core.security import admin_required

router = APIRouter(prefix="/usuarios", tags=["Usuários"])


@router.post(
    "",
    response_model=UserResponse,
    dependencies=[Depends(admin_required)],
)
def criar_usuario(
    data: UserCreate,
    db: Session = Depends(get_db),
):
    return UserService.create_user(
        db,
        username=data.username,
        password=data.password,
        perfil=data.perfil,
    )


@router.get(
    "",
    response_model=list[UserResponse],
    dependencies=[Depends(admin_required)],
)
def listar_usuarios(db: Session = Depends(get_db)):
    return UserService.list_users(db)
