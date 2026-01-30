import os
import uuid

from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload

from app.models.enums import (
    TipoPrincipalSinistro,
    TipoSecundarioSinistro,
)
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
    def create_sinistro(db: Session, data, current_user, files=None):

        files = files or []

        if not data.envolvidos:
            raise HTTPException(400, "Informe ao menos um envolvido")

        tipo_principal, tipo_secundario = SinistroService._inferir_tipos(
            data.envolvidos
        )

        sinistro = Sinistro(
            tipo_principal=tipo_principal,
            tipo_secundario=tipo_secundario,
            descricao_outro=data.descricao_outro,
            endereco=data.endereco,
            ponto_referencia=data.ponto_referencia,
            latitude=data.latitude,
            longitude=data.longitude,
            houve_vitima_fatal=data.houve_vitima_fatal,
            usuario_id=current_user.id,
        )

        db.add(sinistro)
        db.commit()
        db.refresh(sinistro)

        # --------------------------
        # ENVOLVIDOS
        # --------------------------

        for e in data.envolvidos:

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

            elif e.tipo == "pedestre":

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
        # FOTOS
        # --------------------------

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
    # INFERÊNCIA
    # ======================================================

    @staticmethod
    def _inferir_tipos(envolvidos):

        tipos = [e.tipo for e in envolvidos]

        a = tipos[0]
        b = tipos[1] if len(tipos) > 1 else "outro"

        if a == "carro":
            return (
                TipoPrincipalSinistro.CARRO,
                {
                    "carro": TipoSecundarioSinistro.CARRO_CARRO,
                    "moto": TipoSecundarioSinistro.CARRO_MOTO,
                    "pedestre": TipoSecundarioSinistro.CARRO_PEDESTRE,
                }.get(b, TipoSecundarioSinistro.CARRO_OUTRO),
            )

        if a == "moto":
            return (
                TipoPrincipalSinistro.MOTO,
                {
                    "carro": TipoSecundarioSinistro.MOTO_CARRO,
                    "moto": TipoSecundarioSinistro.MOTO_MOTO,
                    "pedestre": TipoSecundarioSinistro.MOTO_PEDESTRE,
                }.get(b, TipoSecundarioSinistro.MOTO_OUTRO),
            )

        return (
            TipoPrincipalSinistro.OUTRO,
            TipoSecundarioSinistro.OUTRO_OUTRO,
        )
        
    @staticmethod
    def get_sinistro(db: Session, sinistro_id: int):

        sinistro = (
            db.query(Sinistro)
            .filter(Sinistro.id == sinistro_id)
            .options(
                joinedload(Sinistro.veiculos).joinedload(Veiculo.condutor),
                joinedload(Sinistro.pedestres),
                joinedload(Sinistro.fotos),
                joinedload(Sinistro.usuario),  # 👈 IMPORTANTE
            )
            .first()
        )

        if not sinistro:
            raise HTTPException(status_code=404, detail="Sinistro não encontrado")

        return serialize_sinistro(sinistro)
