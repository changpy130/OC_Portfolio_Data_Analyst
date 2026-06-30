from fastapi import APIRouter, HTTPException, FastAPI, UploadFile, File
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
import io
from api.utility import _load_model, _predict_bill, _make_result
from api.model import BillRequest

router = APIRouter()
MODEL_PATH = Path("is_genuine_model.pkl")
FEATURES = ["diagonal", "height_left", "height_right", "margin_low", "margin_up", "length"]

@router.get("/health", tags=['Monitoring'], description="Checking if the predictive model is in production")
def check_model():
    if MODEL_PATH.exists():
        try:
            model = _load_model(MODEL_PATH)
            return {"status": "ok", "model_loaded": True, "version": "1.0.0"}
        except RuntimeError as e:
            raise HTTPException(status_code=503, detail=str(e)) 
    else:
        return {
            "message": f"⚠️ Load model error: can't find file at {MODEL_PATH}"
        }

@router.post("/predict", tags=['Prediction'], description="Predicting one bill from a dictionary format")
def predict(data: BillRequest):
    model = _load_model(MODEL_PATH)

    if model is None:
       raise HTTPException(status_code=503, detail="Modèle non disponible")

    values = pd.DataFrame([{
        'diagonal': data.diagonal,
        'height_left':  data.height_left,
        'height_right': data.height_right,
        'margin_low': data.margin_low,
        'margin_up': data.margin_up,
        'length': data.length,
    }])

    result = _make_result(_predict_bill(values, model))

    return result


@router.post("/predict/batch", tags=['Prediction'], description="Predicting bills from a file CSV")
def predict_batch(file: UploadFile, sep=";"):
    model = _load_model(MODEL_PATH)

    if model is None:
       raise HTTPException(status_code=503, detail="Modèle non disponible")

    doc = file.file.read()
    df = pd.read_csv(io.StringIO(doc.decode(encoding="utf-8")), sep=sep)
    df = df[FEATURES]

    colonnes_manquantes = [f for f in FEATURES if f not in df.columns]
    if colonnes_manquantes:
        raise HTTPException(status_code=400, detail=f"Colonnes manquantes : {colonnes_manquantes}")

    result = _make_result(_predict_bill(df, model))

    return result