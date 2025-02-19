from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "FastAPI werkt!"}

@app.get("/vraag/{tekst}")
def antwoord_vraag(tekst: str):
    return {"antwoord": f"Je vroeg: {tekst}"}
