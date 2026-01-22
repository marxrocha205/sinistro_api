import os
import uuid
from fastapi import UploadFile, HTTPException, status
from sqlalchemy.orm import Session

from app.models.sinistro_foto import SinistroFoto
from app.repositories.sinistro_repository import SinistroRepository

UPLOAD_DIR = "app/uploads/sinistros"


class FotoService:

    @staticmethod
    def upload(
        db: Session,
        sinistro_id: int,
        arquivo: UploadFile,
    ) -> SinistroFoto:

        # 1️⃣ Verifica se o sinistro existe
        sinistro = SinistroRepository.get_by_id(db, sinistro_id)
        if not sinistro:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sinistro não encontrado",
            )

        # 2️⃣ Garante pasta
        os.makedirs(UPLOAD_DIR, exist_ok=True)

        # 3️⃣ Gera nome único
        extensao = os.path.splitext(arquivo.filename)[1]
        nome_arquivo = f"{uuid.uuid4()}{extensao}"

        caminho_relativo = f"sinistros/{nome_arquivo}"
        caminho_fisico = os.path.join(UPLOAD_DIR, nome_arquivo)

        # 4️⃣ Salva o arquivo
        with open(caminho_fisico, "wb") as f:
            f.write(arquivo.file.read())

        # 5️⃣ Cria vínculo no banco
        foto = SinistroFoto(
            caminho_arquivo=caminho_relativo,
            sinistro_id=sinistro_id,
        )

        db.add(foto)
        db.commit()
        db.refresh(foto)

        return foto
