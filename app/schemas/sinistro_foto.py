from pydantic import BaseModel
from app.core import config

class SinistroFotoResponse(BaseModel):
    id: int
    url: str
    
    @property
    def url(self) -> str:
        return f"{config.r2_public_url}/{self.caminho_arquivo}"
    class Config:
        from_attributes = True
