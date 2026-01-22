from pydantic import BaseModel, Field
from datetime import datetime
from app.models.enums import TipoPrincipalSinistro, TipoSecundarioSinistro
from app.schemas.sinistro_foto import SinistroFotoResponse


class SinistroCreate(BaseModel):
    tipo_principal: TipoPrincipalSinistro
    tipo_secundario: TipoSecundarioSinistro
    descricao_outro: str | None = None
    latitude: float 
    longitude: float 
    endereco: str
    ponto_referencia: str | None = None
    houve_vitima_fatal: bool = False


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
    
    
