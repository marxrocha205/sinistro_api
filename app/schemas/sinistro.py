from pydantic import BaseModel
from datetime import datetime

from app.models.enums import TipoPrincipalSinistro, TipoSecundarioSinistro
from app.schemas.sinistro_foto import SinistroFotoResponse
from app.core.config import settings


# ✅ ESSE ESTAVA FALTANDO
class SinistroCreate(BaseModel):

    tipo_principal: TipoPrincipalSinistro
    tipo_secundario: TipoSecundarioSinistro
    descricao_outro: str | None
    endereco: str
    ponto_referencia: str | None
    latitude: float
    longitude: float
    houve_vitima_fatal: bool


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

    @classmethod
    def model_validate(cls, obj):

        data = super().model_validate(obj)

        data.fotos = [
            {
                "id": f.id,
                "url": f"{settings.r2_public_url}/{f.caminho_arquivo}",
            }
            for f in obj.fotos
        ]

        return data

    class Config:
        from_attributes = True
