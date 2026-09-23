import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.usuarios import usuarios_router

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

# Incluir las rutas de usuarios
app.include_router(usuarios_router, prefix="/usuarios", tags=["Usuarios"])


@app.get("/")
def raiz():
    return {"mensaje": "API en marcha"}


if __name__ == "__main__":
    uvicorn.run("src.main:app", host="127.0.0.1", port=8000, reload=True)