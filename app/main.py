from fastapi import FastAPI
from app.api.policy_api import router

app = FastAPI(
    title="PolicyHub",
    description="Serviço reutilizavel de políticas de acesso",
    version="1.0.0"
)

app.include_router(router)