from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, Float
)
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database.base import Base
from app.models.enums import TipoPrincipalSinistro, TipoSecundarioSinistro


class Sinistro(Base):
    __tablename__ = "sinistros"

    id = Column(Integer, primary_key=True, index=True)

    tipo_principal = Column(Enum(TipoPrincipalSinistro), nullable=False)
    tipo_secundario = Column(Enum(TipoSecundarioSinistro), nullable=False)
    descricao_outro = Column(String(255), nullable=True)

    endereco = Column(String(255), nullable=False)
    ponto_referencia = Column(String(255), nullable=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    data_hora = Column(DateTime, default=datetime.utcnow)

    houve_vitima_fatal = Column(Boolean, default=False)

    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)

    # 🔗 RELATIONSHIPS
    usuario = relationship("User")

    veiculos = relationship(
        "Veiculo",
        back_populates="sinistro",
        cascade="all, delete-orphan"
    )

    fotos = relationship(
        "SinistroFoto",
        back_populates="sinistro",
        cascade="all, delete-orphan"
    )
    
    pedestres = relationship(
        "Pedestre",
        back_populates="sinistro",
        cascade="all, delete-orphan"
    )
