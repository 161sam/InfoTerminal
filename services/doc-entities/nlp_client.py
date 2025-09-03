import os
import requests

NLP_URL = os.getenv("NLP_URL", "http://127.0.0.1:8405")

def ner(text: str):
    try:
        r = requests.post(f"{NLP_URL}/ner", json={"text": text}, timeout=3)
        r.raise_for_status()
        return r.json().get("entities") or r.json().get("ents", [])
    except Exception:
        return []
