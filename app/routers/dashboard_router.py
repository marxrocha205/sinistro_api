from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date

from app.database.deps import get_db
from app.core.security import get_current_user
from app.models.sinistro import Sinistro
from app.models.user import User
from sqlalchemy import func

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/overview")
def dashboard_overview(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    today = date.today()

    total = db.query(Sinistro).count()

    today_count = (
        db.query(Sinistro)
        .filter(func.date(Sinistro.data_hora) == today)
        .count()
    )

    month_count = (
        db.query(Sinistro)
        .filter(func.month(Sinistro.data_hora) == today.month)
        .count()
    )

    categorias = (
        db.query(
            Sinistro.tipo_principal,
            func.count(Sinistro.id),
        )
        .group_by(Sinistro.tipo_principal)
        .all()
    )

    timeline = (
        db.query(
            func.date(Sinistro.data_hora),
            func.count(Sinistro.id),
        )
        .group_by(func.date(Sinistro.data_hora))
        .order_by(func.date(Sinistro.data_hora))
        .all()
    )

    return {
        "cards": {
            "total": total,
            "today": today_count,
            "month": month_count,
        },
        "categorias": [
            {"label": c[0], "value": c[1]} for c in categorias
        ],
        "timeline": [
            {"date": str(t[0]), "value": t[1]} for t in timeline
        ],
    }
