import uuid
import os

from fastapi import UploadFile, HTTPException, status
from sqlalchemy.orm import Session

from app.models.sinistro_foto import SinistroFoto
from app.repositories.sinistro_repository import SinistroRepository
from app.core.storage.r2client import s3, BUCKET, PUBLIC_URL


class FotoService:

    @staticmethod
    def upload_foto(
        db: Session,
        sinistro_id: int,
        arquivo: UploadFile,
    ) -> SinistroFoto:

        sinistro = SinistroRepository.get_by_id(db, sinistro_id)
        if not sinistro:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sinistro não encontrado",
            )

        ext = os.path.splitext(arquivo.filename)[1]
        filename = f"sinistros/{uuid.uuid4()}{ext}"

        # upload para R2
        s3.upload_fileobj(
            arquivo.file,
            BUCKET,
            filename,
            ExtraArgs={
                "ContentType": arquivo.content_type,
            },
        )

        url = f"{PUBLIC_URL}/{filename}"

        foto = SinistroFoto(
            caminho_arquivo=url,
            sinistro_id=sinistro_id,
        )

        db.add(foto)
        db.commit()
        db.refresh(foto)

        return foto
