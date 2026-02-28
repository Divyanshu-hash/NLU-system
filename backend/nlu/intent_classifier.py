import pickle
import os

class IntentClassifier:
    def __init__(self):
        # Path of this file: backend/nlu/intent_classifier.py
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Go to backend/
        backend_dir = os.path.abspath(os.path.join(current_dir, ".."))

        model_path = os.path.join(backend_dir, "intent_model.pkl")
        vectorizer_path = os.path.join(backend_dir, "tfidf_vectorizer (1).pkl")

        with open(model_path, "rb") as f:
            self.model = pickle.load(f)

        with open(vectorizer_path, "rb") as f:
            self.vectorizer = pickle.load(f)

    def predict(self, text, threshold=0.6):
        X = self.vectorizer.transform([text])
        probs = self.model.predict_proba(X)[0]
        idx = probs.argmax()

        intent = self.model.classes_[idx]
        confidence = probs[idx]

        if confidence < threshold:
            return "fallback", confidence

        return intent, confidence