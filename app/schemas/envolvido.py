from pydantic import BaseModel
from typing import Optional, Literal

from app.schemas.veiculo import VeiculoCreate
from app.schemas.pedestre import PedestreCreate


class EnvolvidoCreate(BaseModel):
    tipo: Literal["carro", "moto", "pedestre", "outro"]

    veiculo: Optional[VeiculoCreate] = None
    pedestre: Optional[PedestreCreate] = None
