from sqlalchemy.orm import Session
from app.models.sinistro_foto import SinistroFoto
from app.models.enums import TipoFoto


class FotoRepository:

    @staticmethod
    def count_by_tipo(db: Session, sinistro_id: int, tipo: TipoFoto):
        return (
            db.query(SinistroFoto)
            .filter(SinistroFoto.sinistro_id == sinistro_id, SinistroFoto.tipo == tipo)
            .count()
        )

    @staticmethod
    def create(db: Session, foto: SinistroFoto):
        db.add(foto)
        db.commit()
        db.refresh(foto)
        return foto
