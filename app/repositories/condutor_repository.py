from sqlalchemy.orm import Session
from app.models.condutor import Condutor


class CondutorRepository:

    @staticmethod
    def create(db: Session, condutor: Condutor):
        db.add(condutor)
        db.commit()
        db.refresh(condutor)
        return condutor
