from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

# Fake klantendatabase
klanten_db: Dict[str, Dict] = {
    "123": {"id": "123", "naam": "Jansen BV", "email": "info@jansenbv.nl", "telefoon": "0612345678"}
}

offertes_db = []

class OfferteIn(BaseModel):
    klantId: str
    beschrijving: str
    bedrag: float

class OfferteOut(BaseModel):
    offerteId: str
    status: str

@app.get("/klanten/{klant_id}")
def get_klant(klant_id: str):
    klant = klanten_db.get(klant_id)
    if klant:
        return klant
    raise HTTPException(status_code=404, detail="Klant niet gevonden")

@app.post("/offertes", response_model=OfferteOut, status_code=201)
def create_offerte(data: OfferteIn):
    offerte_id = f"OFFERTE-{len(offertes_db)+1}"
    offertes_db.append({
        "offerteId": offerte_id,
        "klantId": data.klantId,
        "beschrijving": data.beschrijving,
        "bedrag": data.bedrag
    })
    return {"offerteId": offerte_id, "status": "Aangemaakt"}
