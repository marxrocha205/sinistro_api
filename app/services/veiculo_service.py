from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.veiculo import Veiculo
from app.models.condutor import Condutor
from app.models.enums import TipoVeiculo
from app.repositories.veiculo_repository import VeiculoRepository
from app.repositories.condutor_repository import CondutorRepository
from app.repositories.sinistro_repository import SinistroRepository


class VeiculoService:

    @staticmethod
    def create_veiculo(db: Session, data):

        sinistro = SinistroRepository.get_by_id(db, data.sinistro_id)
        if not sinistro:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sinistro não encontrado",
            )

        if data.tipo == TipoVeiculo.OUTRO and not data.descricao_outro:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Descrição obrigatória para veículo OUTRO",
            )

        veiculo = Veiculo(
            tipo=data.tipo,
            placa=data.placa,
            chassi = data.chassi,
            descricao_outro=data.descricao_outro,
            sinistro_id=data.sinistro_id,
        )

        veiculo = VeiculoRepository.create(db, veiculo)

        if data.condutor:
            condutor = Condutor(
                nome=data.condutor.nome,
                cpf=data.condutor.cpf,
                veiculo_id=veiculo.id,
            )
            CondutorRepository.create(db, condutor)

        return veiculo
