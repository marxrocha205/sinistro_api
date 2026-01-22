from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.core.security import hash_password


class UserService:

    @staticmethod
    def create_user(db: Session, username: str, password: str, perfil: str):
        existing_user = UserRepository.get_by_username(db, username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Usuário já existe",
            )

        user = User(
            username=username,
            senha_hash=hash_password(password),
            perfil=perfil,
        )

        return UserRepository.create(db, user)

    @staticmethod
    def list_users(db: Session):
        return UserRepository.list_all(db)
