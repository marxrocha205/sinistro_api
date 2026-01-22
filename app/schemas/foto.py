from pydantic import BaseModel, Field
from app.models.enums import TipoFoto


class FotoResponse(BaseModel):
    id: int
    tipo: TipoFoto
    descricao: str | None
    caminho_arquivo: str = Field(..., alias="caminho_arquivo")

    class Config:
        from_attributes = True
        populate_by_name = True

    class Config:
        from_attributes = True
