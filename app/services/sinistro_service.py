import os
import uuid
from fastapi import HTTPException, status, UploadFile
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.enums import TipoSecundarioSinistro
from app.models.sinistro import Sinistro
from app.models.sinistro_foto import SinistroFoto
from app.repositories.sinistro_repository import SinistroRepository

from app.core.config import settings
from app.core.storage.r2client import s3, BUCKET


class SinistroService:

    @staticmethod
    def create_sinistro(
        db: Session,
        data,
        current_user: User,
        files: list[UploadFile] | None = None,
    ):

        # ==========================
        # validações
        # ==========================

        if not (-90 <= data.latitude <= 90):
            raise HTTPException(
                status_code=400,
                detail="Latitude inválida",
            )

        if not (-180 <= data.longitude <= 180):
            raise HTTPException(
                status_code=400,
                detail="Longitude inválida",
            )

        if data.tipo_secundario in [
            TipoSecundarioSinistro.CARRO_OUTRO,
            TipoSecundarioSinistro.MOTO_OUTRO,
        ] and not data.descricao_outro:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Descrição obrigatória para tipo OUTRO",
            )

        # ==========================
        # cria sinistro
        # ==========================

        sinistro = Sinistro(
            tipo_principal=data.tipo_principal,
            tipo_secundario=data.tipo_secundario,
            descricao_outro=data.descricao_outro,
            latitude=data.latitude,
            longitude=data.longitude,
            endereco=data.endereco,
            ponto_referencia=data.ponto_referencia,
            houve_vitima_fatal=data.houve_vitima_fatal,
            usuario_id=current_user.id,
        )

        db.add(sinistro)
        db.commit()
        db.refresh(sinistro)

        # ==========================
        # upload R2
        # ==========================

        if not files:
            return sinistro

        for file in files:

            ext = os.path.splitext(file.filename)[1]
            nome = f"{uuid.uuid4()}{ext}"

            object_key = f"sinistros/{sinistro.id}/{nome}"

            print("☁️ R2 UPLOAD:", object_key)

            s3.upload_fileobj(
                file.file,
                BUCKET,
                object_key,
                ExtraArgs={
                    "ContentType": file.content_type,
                },
            )

            foto = SinistroFoto(
                caminho_arquivo=object_key,
                sinistro_id=sinistro.id,
            )

            db.add(foto)

        db.commit()
        db.refresh(sinistro)

        # ==========================
        # monta URL pública
        # ==========================

        for foto in sinistro.fotos:
            foto.url = f"{settings.r2_public_url}/{foto.caminho_arquivo}"

        return sinistro

    # ============================

    @staticmethod
    def list_sinistros(db: Session, skip: int, limit: int):
        return SinistroRepository.list_paginated(db, skip, limit)

    @staticmethod
    def get_sinistro(db: Session, sinistro_id: int):

        sinistro = SinistroRepository.get_by_id(db, sinistro_id)

        if not sinistro:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sinistro não encontrado",
            )

        return sinistro
