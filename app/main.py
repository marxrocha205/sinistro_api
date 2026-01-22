from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import dashboard_router
from fastapi.staticfiles import StaticFiles

from app.routers import (
    auth_router,
    user_router,
    sinistro_router,
    veiculo_router,
    foto_router,
)

app = FastAPI(
    title="API de Sinistros de Trânsito",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, restrinja
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(user_router.router)
app.include_router(sinistro_router.router)
app.include_router(veiculo_router.router)
app.include_router(foto_router.router)
app.include_router(dashboard_router.router)
app.mount("/media", StaticFiles(directory="app/uploads"), name="media")
