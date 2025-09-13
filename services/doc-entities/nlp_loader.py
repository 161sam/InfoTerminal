import os, functools
import spacy

DEFAULT_LANG = os.getenv("NLP_DEFAULT_LANG", "en")
SPACY_EN = os.getenv("NLP_SPACY_MODEL_EN", "en_core_web_sm")
SPACY_DE = os.getenv("NLP_SPACY_MODEL_DE", "de_core_news_sm")
BACKEND   = os.getenv("NLP_BACKEND", "spacy")  # spacy|transformers

@functools.lru_cache(maxsize=4)
def get_nlp(lang: str):
    model = SPACY_EN if lang.startswith("en") else SPACY_DE
    return spacy.load(model)

def ner_spacy(text: str, lang: str):
    nlp = get_nlp(lang)
    doc = nlp(text)
    return [{"text": e.text, "label": e.label_, "start": e.start_char, "end": e.end_char} for e in doc.ents]

def summarize(text: str, lang: str):
    if BACKEND == "transformers":
        try:
            from transformers import pipeline
            pipe = pipeline("summarization", model="facebook/bart-large-cnn")
            return pipe(text[:3000])[0]["summary_text"]
        except Exception:
            pass
    # fallback: naive first sentence
    return (text.split(".")[0] or text)[:500]
