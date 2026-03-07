from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import os
import sys
from pathlib import Path

# Make src importable
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR / "src"))

from process.function import Function
from process.utility import time_format

app = FastAPI()

API_KEY = os.getenv("CREATIONDATE_API_KEY", "")
estimator = Function()

class LookupRequest(BaseModel):
    query: str

@app.get("/health")
async def health():
    return {"ok": True}

@app.post("/lookup")
async def lookup(body: LookupRequest, x_api_key: str = Header(default="")):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="unauthorized")

    raw_query = body.query.strip()

    # For now: support numeric Telegram user IDs only
    try:
        tg_id = int(raw_query)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="This version supports numeric Telegram user IDs only. Username lookup is not connected yet."
        )

    try:
        estimated_unix = int(estimator.func(tg_id))
        estimated_date = time_format(estimated_unix)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Estimator error: {str(e)}")

    return {
        "ok": True,
        "query": raw_query,
        "user_id": tg_id,
        "username": None,
        "creation_date_estimate": estimated_date,
        "confidence": None,
        "method": "creationdate_polynomial_estimator",
        "cached": False
    }
