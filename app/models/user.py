from sqlalchemy import Column, Integer, String, Enum
from app.database.base import Base
from app.models.enums import PerfilUsuario

class User(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    senha_hash = Column(String(255), nullable=False)
    perfil = Column(Enum(PerfilUsuario), nullable=False)
