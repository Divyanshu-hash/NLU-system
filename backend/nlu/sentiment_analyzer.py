from transformers import pipeline

class SentimentAnalyzer:
    def __init__(self):
        self.analyzer = pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english"
        )

    def analyze(self, text):
        r = self.analyzer(text)[0]
        emotion = "neutral"

        if r["label"] == "NEGATIVE" and r["score"] > 0.85:
            emotion = "frustrated"
        elif r["label"] == "POSITIVE" and r["score"] > 0.85:
            emotion = "happy"

        return {
            "label": r["label"],
            "score": round(r["score"], 3),
            "emotion": emotion
        }