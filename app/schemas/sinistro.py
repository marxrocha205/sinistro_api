from pydantic import BaseModel
from datetime import datetime
from app.schemas.envolvido import EnvolvidoCreate
from app.schemas.sinistro_foto import SinistroFotoResponse
from app.models.enums import TipoPrincipalSinistro, TipoSecundarioSinistro


# ==========================
# CREATE
# ==========================

class SinistroCreate(BaseModel):

    descricao_outro: str | None = None

    endereco: str
    ponto_referencia: str | None = None

    latitude: float
    longitude: float

    houve_vitima_fatal: bool = False

    envolvidos: list[EnvolvidoCreate]


# ==========================
# RESPONSE
# ==========================

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
    envolvidos: list[EnvolvidoCreate] = []

    class Config:
        from_attributes = True


# ==========================
# UPDATE
# ==========================

class SinistroUpdate(BaseModel):

    tipo_principal: TipoPrincipalSinistro
    tipo_secundario: TipoSecundarioSinistro

    descricao_outro: str | None

    endereco: str
    ponto_referencia: str | None
    latitude: float
    longitude: float
    houve_vitima_fatal: bool

    envolvidos: list[EnvolvidoCreate] = []
