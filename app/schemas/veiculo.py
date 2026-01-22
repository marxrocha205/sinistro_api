from pydantic import BaseModel
from app.models.enums import TipoVeiculo
from app.schemas.condutor import CondutorCreate, CondutorResponse


class VeiculoCreate(BaseModel):
    sinistro_id: int
    tipo: TipoVeiculo
    placa: str | None = None
    chassi: str | None = None
    descricao_outro: str | None = None
    condutor: CondutorCreate | None = None


class VeiculoResponse(BaseModel):
    id: int
    tipo: TipoVeiculo
    placa: str | None
    chassi: str | None
    descricao_outro: str | None
    sinistro_id: int
    condutor: CondutorResponse | None

    class Config:
        from_attributes = True
