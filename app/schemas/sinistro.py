from pydantic import BaseModel
from datetime import datetime

from app.models.enums import TipoPrincipalSinistro, TipoSecundarioSinistro
from app.schemas.sinistro_foto import SinistroFotoResponse
from app.core.config import Settings


# ===========================
# CREATE
# ===========================

class SinistroCreate(BaseModel):

    tipo_principal: TipoPrincipalSinistro
    tipo_secundario: TipoSecundarioSinistro
    descricao_outro: str | None
    endereco: str
    ponto_referencia: str | None
    latitude: float
    longitude: float
    houve_vitima_fatal: bool


# ===========================
# RESPONSE
# ===========================

class SinistroResponse(BaseModel):

    id: int
    tipo_principal: TipoPrincipalSinistro
    tipo_secundario: TipoSecundarioSinistro
    descricao_outro: str | None
    endereco: str
    latitude: float
    longitude: float
    ponto_referencia: str | None
    houve_vitima_fatal: bool
    data_hora: datetime
    usuario_id: int
    fotos: list[SinistroFotoResponse] = []

    class Config:
        from_attributes = True