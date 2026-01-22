from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session

from app.database.deps import get_db
from app.schemas.foto import FotoResponse
from app.services.foto_service import FotoService
from app.models.enums import TipoFoto
from app.core.security import get_current_user

router = APIRouter(prefix="/fotos", tags=["Fotos"])


@router.post("/upload", response_model=FotoResponse)
def upload_foto(
    sinistro_id: int = Form(...),
    tipo: TipoFoto = Form(...),
    descricao: str | None = Form(None),
    arquivo: UploadFile = File(...),
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    return FotoService.upload_foto(
        db=db,
        sinistro_id=sinistro_id,
        tipo=tipo,
        descricao=descricao,
        arquivo=arquivo,
    )
