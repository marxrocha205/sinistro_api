import os
import uuid

from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload

from app.models.enums import TipoSecundarioSinistro
from app.models.sinistro import Sinistro
from app.models.veiculo import Veiculo
from app.models.condutor import Condutor
from app.models.pedestre import Pedestre
from app.models.sinistro_foto import SinistroFoto

from app.services.sinistro_serializer import serialize_sinistro
from app.core.storage.r2client import s3, BUCKET


class SinistroService:

    # ======================================================
    # CREATE
    # ======================================================

    @staticmethod
    def create_sinistro(
        db: Session,
        data,
        current_user,
        files=None,
    ):

        # --------------------------
        # 🌍 GEO
        # --------------------------

        if not (-90 <= data.latitude <= 90):
            raise HTTPException(400, "Latitude inválida")

        if not (-180 <= data.longitude <= 180):
            raise HTTPException(400, "Longitude inválida")

        if not data.envolvidos:
            raise HTTPException(400, "Informe ao menos um envolvido")

        # --------------------------
        # 🧱 SINISTRO
        # --------------------------

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

        # --------------------------
        # 👥 ENVOLVIDOS
        # --------------------------

        for e in data.envolvidos:

            # ============
            # 🚗 VEÍCULO
            # ============

            if e.tipo in ("carro", "moto"):

                if not e.veiculo:
                    raise HTTPException(400, "Veículo obrigatório")

                v = e.veiculo

                veiculo = Veiculo(
                    tipo=v.tipo,
                    placa=v.placa,
                    chassi=v.chassi,
                    descricao_outro=v.descricao_outro,
                    sinistro_id=sinistro.id,
                )

                db.add(veiculo)
                db.flush()

                if not v.condutor:
                    raise HTTPException(400, "Condutor obrigatório")

                c = v.condutor

                if c.possui_cnh and not c.numero_cnh:
                    raise HTTPException(400, "CNH obrigatória")

                db.add(
                    Condutor(
                        nome=c.nome,
                        cpf=c.cpf,
                        possui_cnh=c.possui_cnh,
                        numero_cnh=c.numero_cnh,
                        veiculo_id=veiculo.id,
                    )
                )

            # ============
            # 🚶 PEDESTRE
            # ============

            if e.tipo == "pedestre":

                if not e.pedestre:
                    raise HTTPException(400, "Pedestre obrigatório")

                p = e.pedestre

                db.add(
                    Pedestre(
                        nome=p.nome,
                        cpf=p.cpf,
                        sinistro_id=sinistro.id,
                    )
                )

        # --------------------------
        # 📸 FOTOS
        # --------------------------

        if files:
            for file in files:

                ext = os.path.splitext(file.filename)[1]
                nome = f"{uuid.uuid4()}{ext}"

                key = f"sinistros/{sinistro.id}/{nome}"

                s3.upload_fileobj(
                    file.file,
                    BUCKET,
                    key,
                    ExtraArgs={"ContentType": file.content_type},
                )

                db.add(
                    SinistroFoto(
                        caminho_arquivo=key,
                        sinistro_id=sinistro.id,
                    )
                )

        db.commit()

        sinistro = (
            db.query(Sinistro)
            .filter(Sinistro.id == sinistro.id)
            .options(
                joinedload(Sinistro.veiculos).joinedload(Veiculo.condutor),
                joinedload(Sinistro.pedestres),
                joinedload(Sinistro.fotos),
            )
            .first()
        )

        return serialize_sinistro(sinistro)

    # ======================================================
    # GET
    # ======================================================

    @staticmethod
    def get_sinistro(db: Session, sinistro_id: int):

        sinistro = (
            db.query(Sinistro)
            .filter(Sinistro.id == sinistro_id)
            .options(
                joinedload(Sinistro.veiculos).joinedload(Veiculo.condutor),
                joinedload(Sinistro.pedestres),
                joinedload(Sinistro.fotos),
            )
            .first()
        )

        if not sinistro:
            raise HTTPException(404, "Sinistro não encontrado")

        return serialize_sinistro(sinistro)

    # ======================================================
    # DELETE
    # ======================================================

    @staticmethod
    def delete_sinistro(db: Session, sinistro_id: int, current_user):

        sinistro = (
            db.query(Sinistro)
            .filter(Sinistro.id == sinistro_id)
            .first()
        )

        if not sinistro:
            raise HTTPException(404, "Sinistro não encontrado")

        if (
            current_user.perfil != "ADMIN"
            and sinistro.usuario_id != current_user.id
        ):
            raise HTTPException(403, "Sem permissão")

        for foto in sinistro.fotos:
            try:
                s3.delete_object(
                    Bucket=BUCKET,
                    Key=foto.caminho_arquivo,
                )
            except Exception as e:
                print("⚠️ erro R2:", e)

        db.delete(sinistro)
        db.commit()
