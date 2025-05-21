from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

class MemoIn(BaseModel):
    tekst: str

class MemoSamenvatting(BaseModel):
    onderzoek: str
    herstel: str
    evaluatie: str
    tijdlijn: str
    betrokkenen: str
    juridisch: str

@app.post("/verwerk_memo", response_model=MemoSamenvatting)
def verwerk_memo(data: MemoIn):
    # Placeholder logica
    return {
        "onderzoek": "Geen informatie beschikbaar",
        "herstel": "Geen informatie beschikbaar",
        "evaluatie": "Geen informatie beschikbaar",
        "tijdlijn": "Geen informatie beschikbaar",
        "betrokkenen": "Geen informatie beschikbaar",
        "juridisch": "Geen informatie beschikbaar"
    }
