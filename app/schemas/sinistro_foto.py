from pydantic import BaseModel


class SinistroFotoResponse(BaseModel):
    id: int
    caminho_arquivo: str

    class Config:
        from_attributes = True
