# app/database/base.py
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

from app.models.veiculo import Veiculo
from app.models.condutor import Condutor
from app.models.user import User
from app.models.sinistro import Sinistro
