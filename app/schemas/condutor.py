from typing import Optional
from pydantic import BaseModel


class CondutorCreate(BaseModel):

    nome: str
    cpf: str
    possui_cnh: bool = False
    numero_cnh: Optional[str] = None

class CondutorResponse(BaseModel):

    id: int
    nome: str
    cpf: str
    possui_cnh: bool = False
    numero_cnh: Optional[str] = None
    
    class Config:
        from_attributes = True
