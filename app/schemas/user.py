from pydantic import BaseModel
from app.models.enums import PerfilUsuario


class UserCreate(BaseModel):
    username: str
    password: str
    perfil: PerfilUsuario


class UserResponse(BaseModel):
    id: int
    username: str
    perfil: PerfilUsuario

    class Config:
        from_attributes = True
