from fastapi import FastAPI, Query, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
import joblib
import time
import numpy as np

app = FastAPI()

# ===== CORS =====
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== Load models =====
BASE_DIR = Path(__file__).resolve().parent

MODEL_FILES = {
    "v1": BASE_DIR / "model" / "LogisticRegression_model.joblib",
    "v2": BASE_DIR / "model" / "Linearsvc_model.joblib",
}

DEFAULT_MODEL = "v1"

# โหลดโมเดลจริง (ไม่ใช่ path)
MODELS = {}
for k, p in MODEL_FILES.items():
    if not p.exists():
        raise FileNotFoundError(f"Missing model file: {p}")
    MODELS[k] = joblib.load(p)

# ===== Schema =====
class PredictRequest(BaseModel):
    body: str

class PredictResponse(BaseModel):
    label: str
    confidence: float
    latency_ms: float
    model_version: str

# (กัน OPTIONS 405 แบบชัวร์)
@app.options("/predict")
def options_predict():
    return Response(status_code=200)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/model/info")
def model_info():
    return {
        "available_models": list(MODELS.keys()),
        "default": DEFAULT_MODEL
    }

def predict_with_confidence(m, text: str):
    # ถ้ามี predict_proba (LogReg)
    if hasattr(m, "predict_proba"):
        probs = m.predict_proba([text])[0]
        idx = int(np.argmax(probs))
        return m.classes_[idx], float(probs[idx])

    # ถ้าไม่มี predict_proba แต่มี decision_function (เช่น LinearSVC)
    if hasattr(m, "decision_function"):
        scores = m.decision_function([text])
        scores = scores[0] if hasattr(scores, "__len__") else np.array([scores])
        idx = int(np.argmax(scores))
        exps = np.exp(scores - np.max(scores))
        probs = exps / np.sum(exps)
        return m.classes_[idx], float(probs[idx])

    # fallback
    return m.predict([text])[0], 0.0

@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest, model: str = Query(DEFAULT_MODEL)):
    if model not in MODELS:
        raise HTTPException(status_code=400, detail=f"Unknown model '{model}'. Use: {list(MODELS.keys())}")

    text = (req.body or "").strip()
    if not text:
        raise HTTPException(status_code=400, detail="body is required")

    m = MODELS[model]  # ✅ ตอนนี้เป็นโมเดลจริง
    start = time.time()

    label, confidence = predict_with_confidence(m, text)

    latency_ms = (time.time() - start) * 1000

    return {
        "label": label,
        "confidence": round(confidence, 4),
        "latency_ms": round(latency_ms, 2),
        "model_version": model
    }
