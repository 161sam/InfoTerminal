import re
from fastapi import FastAPI
from pydantic import BaseModel

# Minimal NLP endpoints for NER and summarization

app = FastAPI(title="NLP Service (MVP)")

class TextIn(BaseModel):
    text: str

@app.get("/healthz")
def health():
    return {"status":"ok"}

@app.post("/ner")
def ner(inp: TextIn):
    ents=[]
    for m in re.finditer(r"\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b", inp.text):
        ents.append({"text": m.group(1), "label": "PROPN", "start": m.start(), "end": m.end()})
    return {"ents": ents}

@app.post("/summarize")
def summarize(inp: TextIn):
    t = inp.text.strip().replace("\n"," ")
    return {"summary": t[:200] + ("..." if len(t) > 200 else "")}
