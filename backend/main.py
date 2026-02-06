from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import time
import numpy as np
app = FastAPI()
# ================= Load model =================
MODEL_PATH = "model/tfidf_logreg_model.joblib"
model = joblib.load(MODEL_PATH)

MODEL_VERSION = "1.0.0"

# ================= Schema =================
class PredictRequest(BaseModel):
    body: str

class PredictResponse(BaseModel):
    label: str
    confidence: float
    latency_ms: float
    model_version: str

# ================= API =================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # ใช้ "*" ตอน dev
    allow_credentials=True,
    allow_methods=["*"],      # อนุญาต OPTIONS, POST, GET
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/model/info")
def model_info():
    return {
        "model_type": "TF-IDF + Logistic Regression",
        "version": MODEL_VERSION
    }

@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    start = time.time()

    text =  req.body

    probs = model.predict_proba([text])[0]
    pred_idx = np.argmax(probs)
    label = model.classes_[pred_idx]
    confidence = float(probs[pred_idx])

    latency = (time.time() - start) * 1000

    return {
        "label": label,
        "confidence": round(confidence, 4),
        "latency_ms": round(latency, 2),
        "model_version": MODEL_VERSION
    }

