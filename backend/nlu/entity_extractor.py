import re
import spacy

class EntityExtractor:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def extract(self, text: str):
        doc = self.nlp(text)
        entities = {}

        # ---------- spaCy entities (FILTERED) ----------
        for ent in doc.ents:
            # Keep MONEY only if it contains currency symbol
            if ent.label_ == "MONEY" and any(sym in ent.text for sym in ["₹", "$", "€"]):
                entities["AMOUNT"] = ent.text

            # Keep DATE only if it has alphabet (e.g. yesterday, 12 Jan)
            elif ent.label_ == "DATE" and re.search(r"[a-zA-Z]", ent.text):
                entities["DATE"] = ent.text

        # ---------- Order ID (context-aware regex) ----------
        order_id = re.search(
            r"(order|order id|order number)\s*(is|:)?\s*(\d{4,})",
            text,
            re.IGNORECASE
        )
        if order_id:
            entities["ORDER_ID"] = order_id.group(3)

        # ---------- Email ----------
        email = re.search(r"\b[\w\.-]+@[\w\.-]+\.\w+\b", text)
        if email:
            entities["EMAIL"] = email.group()

        # ---------- Phone (India) ----------
        phone = re.search(r"\b[6-9]\d{9}\b", text)
        if phone:
            entities["PHONE"] = phone.group()

        return entities