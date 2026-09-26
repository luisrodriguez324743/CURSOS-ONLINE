import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.usuarios import usuarios_router
from src.api.roles import roles_router
from src.api.resenas import resenas_router
from src.api.cursos import cursos_router
from src.api.modulos import modulos_router
from src.api.lecciones import lecciones_router

app = FastAPI(
    title="CURSO-ONLINE",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En desarrollo; ajustar en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar routers
app.include_router(usuarios_router)
app.include_router(roles_router)
app.include_router(resenas_router)
app.include_router(cursos_router)
app.include_router(modulos_router)
app.include_router(lecciones_router)


@app.get("/")
def raiz():
    return {"mensaje": "API en marcha"}


if __name__ == "__main__":
    uvicorn.run("src.main:app", host="127.0.0.1", port=8000, reload=True)
