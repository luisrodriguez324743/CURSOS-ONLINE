from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.endpoints import (
    router_evaluaciones,
    router_inscripciones,
    router_progresos,
)


app = FastAPI(
    title="API Cursos Online",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router_inscripciones)
app.include_router(router_progresos)
app.include_router(router_evaluaciones)


@app.get("/")
def inicio() -> dict[str, str]:
    return {"mensaje": "API Cursos Online funcionando"}
