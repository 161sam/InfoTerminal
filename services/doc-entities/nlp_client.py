from nlp_loader import ner_spacy

def ner(text: str, lang: str = "en"):
    return ner_spacy(text, lang)
