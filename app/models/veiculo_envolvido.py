from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship

from app.database.base import Base
from app.models.enums import TipoVeiculo


class VeiculoEnvolvido(Base):
    __tablename__ = "veiculos_envolvidos"

    id = Column(Integer, primary_key=True)

    sinistro_id = Column(Integer, ForeignKey("sinistros.id"), nullable=False)

    tipo = Column(Enum(TipoVeiculo), nullable=False)

    placa = Column(String(20), nullable=True)

    condutor_nome = Column(String(120), nullable=True)
    condutor_cpf = Column(String(14), nullable=True)

    sinistro = relationship("Sinistro", back_populates="veiculos")
