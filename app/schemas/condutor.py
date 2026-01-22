from pydantic import BaseModel

class CondutorCreate(BaseModel):
    nome: str
    cpf: str


class CondutorResponse(BaseModel):
    id: int
    nome: str
    cpf: str

    class Config:
        from_attributes = True
