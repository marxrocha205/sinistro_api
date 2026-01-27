from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database.base import Base


class Pedestre(Base):
    __tablename__ = "pedestres"

    id = Column(Integer, primary_key=True)

    sinistro_id = Column(Integer, ForeignKey("sinistros.id"), nullable=False)

    nome = Column(String(120), nullable=False)
    cpf = Column(String(14), nullable=False)

    sinistro = relationship("Sinistro", back_populates="pedestres")
