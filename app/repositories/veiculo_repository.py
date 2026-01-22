from sqlalchemy.orm import Session
from app.models.veiculo import Veiculo


class VeiculoRepository:

    @staticmethod
    def create(db: Session, veiculo: Veiculo):
        db.add(veiculo)
        db.commit()
        db.refresh(veiculo)
        return veiculo
