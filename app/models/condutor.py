from xmlrpc.client import Boolean
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base import Base

class Condutor(Base):
    __tablename__ = "condutores"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=True)
    cpf = Column(String(14), nullable=True)
    possui_cnh = Column(Boolean, default=False)
    numero_cnh = Column(String(50), nullable=True)

    veiculo_id = Column(Integer, ForeignKey("veiculos.id", ondelete="CASCADE"), nullable=False)

    veiculo = relationship("Veiculo", back_populates="condutor")

