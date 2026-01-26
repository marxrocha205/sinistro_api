from sqlalchemy.orm import Session, joinedload
from app.models.sinistro import Sinistro


class SinistroRepository:

    @staticmethod
    def create(db: Session, sinistro: Sinistro):
        db.add(sinistro)
        db.commit()
        db.refresh(sinistro)
        return sinistro

    @staticmethod
    def list_paginated(db: Session, skip: int, limit: int):
        return (
            db.query(Sinistro)
            .order_by(Sinistro.data_hora.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_by_id(db: Session, sinistro_id: int):
        return (
            db.query(Sinistro)
            .filter(Sinistro.id == sinistro_id)
            .options(joinedload(Sinistro.fotos))
            .first()
        )
