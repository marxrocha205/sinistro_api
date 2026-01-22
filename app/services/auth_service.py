from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.user_repository import UserRepository
from app.core.security import verify_password, create_access_token

class AuthService:

    @staticmethod
    def login(db: Session, username: str, password: str):
        user = UserRepository.get_by_username(db, username)

        if not user or not verify_password(password, user.senha_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuário ou senha inválidos",
            )

        token = create_access_token({
            "sub": str(user.id),
            "perfil": user.perfil,
        })
        return {"access_token": token, "token_type": "bearer"}
