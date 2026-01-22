from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base import Base


class SinistroFoto(Base):
    __tablename__ = "sinistro_fotos"

    id = Column(Integer, primary_key=True, index=True)
    caminho_arquivo = Column(String(255), nullable=False)

    sinistro_id = Column(Integer, ForeignKey("sinistros.id"), nullable=False)

    sinistro = relationship("Sinistro", back_populates="fotos")
