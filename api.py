from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import os

app = FastAPI()

API_KEY = os.getenv("CREATIONDATE_API_KEY", "")

class LookupRequest(BaseModel):
    query: str

@app.get("/health")
async def health():
    return {"ok": True}

@app.post("/lookup")
async def lookup(body: LookupRequest, x_api_key: str = Header(default="")):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="unauthorized")

    # TODO: call the existing bot/Telethon logic here
    return {
        "ok": True,
        "query": body.query,
        "user_id": 123456789,
        "username": body.query.lstrip("@"),
        "creation_date_estimate": "2018-04-12",
        "confidence": 0.78,
        "method": "telethon_lookup",
        "cached": False
    }
