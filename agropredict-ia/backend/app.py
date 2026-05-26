from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field


BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "model.pkl"

CULTIVOS = {
    0: "Papa",
    1: "Maíz",
    2: "Trigo",
}

TIPOS_SUELO = {
    0: "Arenoso",
    1: "Arcilloso",
    2: "Franco",
}

app = FastAPI(
    title="AgroPredict IA API",
    description="API de recomendación de cultivos para agricultores colombianos.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class PredictionRequest(BaseModel):
    ph: float = Field(..., ge=0, le=14, description="Nivel de pH del suelo")
    humedad: float = Field(..., ge=0, le=100, description="Humedad del suelo en porcentaje")
    temperatura: float = Field(..., ge=-20, le=60, description="Temperatura ambiente en grados Celsius")
    tipo_suelo: int = Field(..., ge=0, le=2, description="0=Arenoso, 1=Arcilloso, 2=Franco")


class PredictionResponse(BaseModel):
    cultivo_recomendado: str
    codigo_cultivo: int


def load_model():
    if not MODEL_PATH.exists():
        raise RuntimeError(
            "No se encontró model.pkl. Ejecuta primero: python train_model.py"
        )

    return joblib.load(MODEL_PATH)


model = load_model()


@app.get("/")
def health_check():
    return {
        "message": "AgroPredict IA API está funcionando",
        "docs": "/docs",
        "tipos_suelo": TIPOS_SUELO,
    }


@app.post("/predict", response_model=PredictionResponse)
def predict_crop(payload: PredictionRequest):
    try:
        input_data = pd.DataFrame(
            [
                {
                    "ph": payload.ph,
                    "humedad": payload.humedad,
                    "temperatura": payload.temperatura,
                    "tipo_suelo": payload.tipo_suelo,
                }
            ]
        )
        prediction = int(model.predict(input_data)[0])

        return {
            "cultivo_recomendado": CULTIVOS[prediction],
            "codigo_cultivo": prediction,
        }
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"No fue posible generar la predicción: {exc}",
        ) from exc
