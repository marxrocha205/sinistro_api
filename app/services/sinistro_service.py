import os,uuid
import uuid
from fastapi import HTTPException, status, UploadFile
from sqlalchemy.orm import Session

from app.models.enums import TipoSecundarioSinistro, TipoVeiculo
from app.models.sinistro import Sinistro
from app.models.veiculo import Veiculo
from app.models.condutor import Condutor
from app.models.pedestre import Pedestre
from app.models.sinistro_foto import SinistroFoto
from app.services.sinistro_serializer import serialize_sinistro

from app.core.config import settings
from app.core.storage.r2client import s3, BUCKET


class SinistroService:

    @staticmethod
    def create_sinistro(
        db: Session,
        data,
        current_user,
        files=None,
    ):

        # ==========================
        # 🌍 VALIDAÇÕES GEO
        # ==========================

        if not (-90 <= data.latitude <= 90):
            raise HTTPException(400, "Latitude inválida")

        if not (-180 <= data.longitude <= 180):
            raise HTTPException(400, "Longitude inválida")

        # ==========================
        # 🧠 VALIDAÇÃO POR TIPO
        # ==========================

        veiculos = data.veiculos or []
        pedestres = data.pedestres or []

        tipo = data.tipo_secundario

        def count_tipo(t):
            return len([v for v in veiculos if v.tipo == t])

        if tipo == TipoSecundarioSinistro.CARRO_CARRO:
            if count_tipo(TipoVeiculo.CARRO) != 2:
                raise HTTPException(400, "CARRO_CARRO exige 2 carros")

        if tipo == TipoSecundarioSinistro.CARRO_MOTO:
            if count_tipo(TipoVeiculo.CARRO) != 1 or count_tipo(TipoVeiculo.MOTO) != 1:
                raise HTTPException(400, "CARRO_MOTO exige 1 carro e 1 moto")

        if tipo == TipoSecundarioSinistro.CARRO_PEDESTRE:
            if not pedestres:
                raise HTTPException(400, "CARRO_PEDESTRE exige pedestre")

        if tipo == TipoSecundarioSinistro.CARRO_OUTRO:
            if not data.descricao_outro:
                raise HTTPException(400, "Descrição obrigatória")

        if tipo == TipoSecundarioSinistro.MOTO_MOTO:
            if count_tipo(TipoVeiculo.MOTO) != 2:
                raise HTTPException(400, "MOTO_MOTO exige 2 motos")

        if tipo == TipoSecundarioSinistro.MOTO_CARRO:
            if count_tipo(TipoVeiculo.MOTO) != 1 or count_tipo(TipoVeiculo.CARRO) != 1:
                raise HTTPException(400, "MOTO_CARRO exige 1 moto e 1 carro")

        if tipo == TipoSecundarioSinistro.MOTO_PEDESTRE:
            if not pedestres:
                raise HTTPException(400, "MOTO_PEDESTRE exige pedestre")

        if tipo == TipoSecundarioSinistro.MOTO_OUTRO:
            if not data.descricao_outro:
                raise HTTPException(400, "Descrição obrigatória")

        # ==========================
        # 🧱 CRIA SINISTRO
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
        # 🚗 VEÍCULOS + CONDUTORES
        # ==========================

        for v in veiculos:

            veiculo = Veiculo(
                tipo=v.tipo,
                placa=v.placa,
                chassi=v.chassi,
                descricao_outro=v.descricao_outro,
                sinistro_id=sinistro.id,
            )

            db.add(veiculo)
            db.flush()

            if v.condutor:
                condutor = Condutor(
                    nome=v.condutor.nome,
                    cpf=v.condutor.cpf,
                    veiculo_id=veiculo.id,
                )
                db.add(condutor)

        # ==========================
        # 🚶 PEDESTRES
        # ==========================

        for p in pedestres:
            pedestre = Pedestre(
                nome=p.nome,
                cpf=p.cpf,
                sinistro_id=sinistro.id,
            )
            db.add(pedestre)

        # ==========================
        # 📸 UPLOAD FOTOS
        # ==========================

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

                foto = SinistroFoto(
                    caminho_arquivo=key,
                    sinistro_id=sinistro.id,
                )
                db.add(foto)

        db.commit()
        db.refresh(sinistro)

        
        return serialize_sinistro(sinistro)
    
    @staticmethod
    def update_sinistro(
        db: Session,
        sinistro_id: int,
        data,
        current_user,
        files=None,
    ):

        sinistro = db.query(Sinistro).filter_by(id=sinistro_id).first()

        if not sinistro:
            raise HTTPException(404, "Sinistro não encontrado")

        # ==========================
        # 🔁 ATUALIZA CAMPOS
        # ==========================

        sinistro.tipo_principal = data.tipo_principal
        sinistro.tipo_secundario = data.tipo_secundario
        sinistro.descricao_outro = data.descricao_outro
        sinistro.endereco = data.endereco
        sinistro.ponto_referencia = data.ponto_referencia
        sinistro.latitude = data.latitude
        sinistro.longitude = data.longitude
        sinistro.houve_vitima_fatal = data.houve_vitima_fatal

        # ==========================
        # 💣 LIMPA ANTIGOS
        # ==========================

        sinistro.veiculos.clear()
        sinistro.pedestres.clear()

        db.flush()

        # ==========================
        # 🧠 REVALIDA REGRAS
        # ==========================

        veiculos = data.veiculos or []
        pedestres = data.pedestres or []

        tipo = data.tipo_secundario

        def count_tipo(t):
            return len([v for v in veiculos if v.tipo == t])

        if tipo == TipoSecundarioSinistro.CARRO_CARRO and count_tipo(TipoVeiculo.CARRO) != 2:
            raise HTTPException(400, "CARRO_CARRO exige 2 carros")

        if tipo == TipoSecundarioSinistro.CARRO_PEDESTRE and not pedestres:
            raise HTTPException(400, "CARRO_PEDESTRE exige pedestre")

        if tipo == TipoSecundarioSinistro.CARRO_OUTRO and not data.descricao_outro:
            raise HTTPException(400, "Descrição obrigatória")

        # ==========================
        # 🚗 RECRIA
        # ==========================

        for v in veiculos:

            veiculo = Veiculo(
                tipo=v.tipo,
                placa=v.placa,
                chassi=v.chassi,
                descricao_outro=v.descricao_outro,
                sinistro_id=sinistro.id,
            )

            db.add(veiculo)
            db.flush()

            if v.condutor:
                condutor = Condutor(
                    nome=v.condutor.nome,
                    cpf=v.condutor.cpf,
                    veiculo_id=veiculo.id,
                )
                db.add(condutor)

        for p in pedestres:
            pedestre = Pedestre(
                nome=p.nome,
                cpf=p.cpf,
                sinistro_id=sinistro.id,
            )
            db.add(pedestre)

        # ==========================
        # 📸 NOVAS FOTOS
        # ==========================

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
        db.refresh(sinistro)

        return serialize_sinistro(sinistro)


    @staticmethod
    def delete_sinistro(
        db: Session,
        sinistro_id: int,
        current_user,
    ):

        sinistro = (
            db.query(Sinistro)
            .filter(Sinistro.id == sinistro_id)
            .first()
        )

        if not sinistro:
            raise HTTPException(404, "Sinistro não encontrado")

        # 🔐 permissão (opcional)
        if (
            current_user.perfil != "ADMIN"
            and sinistro.usuario_id != current_user.id
        ):
            raise HTTPException(403, "Sem permissão")

        # ==========================
        # 🧹 remove arquivos do R2
        # ==========================

        for foto in sinistro.fotos:
            try:
                s3.delete_object(
                    Bucket=BUCKET,
                    Key=foto.caminho_arquivo,
                )
            except Exception as e:
                print("⚠️ Erro removendo R2:", e)

        # ==========================
        # 🧨 remove DB (cascade)
        # ==========================

        db.delete(sinistro)
        db.commit()