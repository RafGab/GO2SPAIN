from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.study_leads import router as study_leads_router
from routes.reviews import router as reviews_router
from database import create_tables

app = FastAPI()

create_tables()  # Crea las tablas si todavía no existen

app.add_middleware(
    CORSMiddleware,
    # allow_origins=["*"] porque la página ACERO PULIDO se sirve desde
    # claude.ai (dominio distinto a este backend); no se usan
    # cookies/credenciales, solo JSON.
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def inicio():
    return {"mensaje": "ACERO PULIDO backend está funcionando 🚀"}


app.include_router(study_leads_router)
app.include_router(reviews_router)
