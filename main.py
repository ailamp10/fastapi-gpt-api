from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os

app = FastAPI()

# Zet hier je eigen OpenAI API sleutel
openai.api_key = os.getenv("OPENAI_API_KEY")

class MemoIn(BaseModel):
    tekst: str

class MemoSamenvatting(BaseModel):
    onderzoek: str
    herstel: str
    evaluatie: str
    tijdlijn: str
    betrokkenen: str
    juridisch: str

INSTRUCTIES = """Je bent een zakelijke assistent die klachtenmemo's verwerkt in zes vaste onderdelen:
1. Onderzoek van de klacht (door de klachteigenaar)
2. Herstel en uitvoering (door leidinggevende of MT)
3. Evaluatie, communicatie en verbetermaatregelen
4. Tijdlijn van gebeurtenissen
5. Betrokken personen of afdelingen
6. Juridische implicaties

Vat helder en beknopt samen wat relevant is voor elk onderdeel. Wees zakelijk, vermijd subjectieve taal, meld expliciet als informatie ontbreekt, en structureer de output altijd in bovenstaande zes categorieën. Redeneer logisch als de informatie impliciet is.
"""

@app.post("/verwerk_memo", response_model=MemoSamenvatting)
def verwerk_memo(data: MemoIn):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": INSTRUCTIES},
            {"role": "user", "content": data.tekst}
        ]
    )
    output = response["choices"][0]["message"]["content"]

    # Verwacht output in vaste volgorde gescheiden door dubbele nieuwe regels
    parts = output.split("\n\n")
    labels = ["onderzoek", "herstel", "evaluatie", "tijdlijn", "betrokkenen", "juridisch"]
    parsed = dict(zip(labels, ["Geen informatie beschikbaar"] * 6))

    for part in parts:
        for label in labels:
            if part.lower().startswith(label):
                parsed[label] = part[len(label)+2:].strip()  # verwijder label + ": "
    return parsed
