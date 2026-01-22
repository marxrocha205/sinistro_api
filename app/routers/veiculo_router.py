from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.deps import get_db
from app.schemas.veiculo import VeiculoCreate, VeiculoResponse
from app.services.veiculo_service import VeiculoService
from app.core.security import get_current_user

router = APIRouter(prefix="/veiculos", tags=["Veículos"])


@router.post("", response_model=VeiculoResponse)
def adicionar_veiculo(
    data: VeiculoCreate,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    return VeiculoService.create_veiculo(db, data)
