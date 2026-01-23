from pydantic import BaseModel


class SinistroFotoResponse(BaseModel):
    id: int
    url: str

    class Config:
        from_attributes = True
