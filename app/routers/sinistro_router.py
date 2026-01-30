from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date
import json

from app.database.deps import get_db
from app.schemas.sinistro import SinistroCreate, SinistroResponse, SinistroUpdate
from app.services.sinistro_service import SinistroService
from app.core.security import get_current_user
from app.models.user import User
from app.models.sinistro import Sinistro
from app.models.enums import (
    TipoPrincipalSinistro,
    TipoSecundarioSinistro,
)

router = APIRouter(prefix="/sinistros", tags=["Sinistros"])


# ✅ CREATE SINISTRO + FOTOS (JUNTOS)
@router.post("/", response_model=dict)
def criar_sinistro(
    descricao_outro: str | None = Form(None),
    endereco: str = Form(...),
    ponto_referencia: str | None = Form(None),
    latitude: float = Form(...),
    longitude: float = Form(...),
    houve_vitima_fatal: bool = Form(False),

    payload: str = Form(...),  # JSON com envolvidos

    files: list[UploadFile] | None = File(None),

    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        payload_data = json.loads(payload)
    except Exception:
        raise HTTPException(400, "Payload inválido")

    data = SinistroCreate(
        descricao_outro=descricao_outro,
        endereco=endereco,
        ponto_referencia=ponto_referencia,
        latitude=latitude,
        longitude=longitude,
        houve_vitima_fatal=houve_vitima_fatal,
        envolvidos=payload_data.get("envolvidos", []),
    )

    return SinistroService.create_sinistro(
        db=db,
        data=data,
        current_user=current_user,
        files=files,
    )

# 📄 LISTAGEM
@router.get("/")
def listar_sinistros(
    skip: int = 0,
    limit: int = 20,
    tipo: str | None = None,
    usuario_id: int | None = None,
    data_ini: date | None = None,
    data_fim: date | None = None,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    query = db.query(Sinistro)

    if tipo:
        query = query.filter(Sinistro.tipo_principal == tipo)

    if usuario_id:
        query = query.filter(Sinistro.usuario_id == usuario_id)

    if data_ini:
        query = query.filter(func.date(Sinistro.data_hora) >= data_ini)

    if data_fim:
        query = query.filter(func.date(Sinistro.data_hora) <= data_fim)

    total = query.count()
 
    items = (
        query
        .order_by(Sinistro.data_hora.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    return {
        "total": total,
        "items": items,
    }
@router.get("/mapa")
def sinistros_mapa(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    sinistros = (
        db.query(Sinistro)
        .filter(
            Sinistro.latitude.isnot(None),
            Sinistro.longitude.isnot(None)
        )
        .all()
    )

    return [
        {
            "id": s.id,
            "tipo": s.tipo_principal,
            "endereco": s.endereco,
            "latitude": s.latitude,
            "longitude": s.longitude,
            "data": s.data_hora.isoformat(),
        }
        for s in sinistros
    ]


# 🔍 DETALHE (JÁ VEM COM FOTOS)
@router.get("/{sinistro_id}", response_model=SinistroResponse)
def detalhar_sinistro(
    sinistro_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    return SinistroService.get_sinistro(db, sinistro_id)



@router.put("/{sinistro_id}", response_model=SinistroResponse)
def atualizar_sinistro(
    sinistro_id: int,
    tipo_principal: TipoPrincipalSinistro = Form(...),
    tipo_secundario: TipoSecundarioSinistro = Form(...),
    descricao_outro: str | None = Form(None),
    endereco: str = Form(...),
    ponto_referencia: str | None = Form(None),
    latitude: float = Form(...),
    longitude: float = Form(...),
    houve_vitima_fatal: bool = Form(False),

    veiculos: str = Form("[]"),
    pedestres: str = Form("[]"),

    files: list[UploadFile] | None = File(None),

    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    data = SinistroUpdate(
        tipo_principal=tipo_principal,
        tipo_secundario=tipo_secundario,
        descricao_outro=descricao_outro,
        endereco=endereco,
        ponto_referencia=ponto_referencia,
        latitude=latitude,
        longitude=longitude,
        houve_vitima_fatal=houve_vitima_fatal,
        veiculos=json.loads(veiculos),
        pedestres=json.loads(pedestres),
    )

    return SinistroService.update_sinistro(
        db=db,
        sinistro_id=sinistro_id,
        data=data,
        current_user=current_user,
        files=files,
    )

@router.delete("/{sinistro_id}")
def deletar_sinistro(
    sinistro_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    SinistroService.delete_sinistro(
        db=db,
        sinistro_id=sinistro_id,
        current_user=current_user,
    )

    return {"message": "Sinistro removido com sucesso"}
