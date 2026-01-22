from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base import Base
from app.models.enums import TipoVeiculo

class Veiculo(Base):
    __tablename__ = "veiculos"

    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(Enum(TipoVeiculo), nullable=False)
    placa = Column(String(10), nullable=True)
    chassi = Column(String(17), nullable = True)
    descricao_outro = Column(String(255), nullable=True)

    sinistro_id = Column(Integer, ForeignKey("sinistros.id"), nullable=False)

    sinistro = relationship("Sinistro", back_populates="veiculos")
    condutor = relationship("Condutor", back_populates="veiculo", uselist=False)
