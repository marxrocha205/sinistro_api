from pydantic import BaseModel


class PedestreCreate(BaseModel):

    nome: str
    cpf: str


class PedestreResponse(BaseModel):

    id: int
    nome: str
    cpf: str

    class Config:
        from_attributes = True
