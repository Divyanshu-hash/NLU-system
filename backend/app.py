from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
load_dotenv()
import os

from groq import Groq

# ---------- NLU Imports ----------
from nlu.intent_classifier import IntentClassifier
from nlu.sentiment_analyzer import SentimentAnalyzer
from nlu.entity_extractor import EntityExtractor
from nlu.decision_layer import DecisionLayer
from nlu.context_manager import ContextManager
from nlu.action_executor import ActionExecutor



# ---------- App ----------
app = FastAPI(title="Context-Aware NLU System")

# ---------- Load NLU Components ----------
intent_clf = IntentClassifier()
sentiment_analyzer = SentimentAnalyzer()
entity_extractor = EntityExtractor()
decision_layer = DecisionLayer()
context_manager = ContextManager()
action_executor = ActionExecutor()


# ---------- Groq Client ----------
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

MODEL_NAME = "meta-llama/llama-4-maverick-17b-128e-instruct"

# ---------- Request Schema ----------
class ChatRequest(BaseModel):
    user_id: str
    text: str

# ---------- LLM Response Generator ----------
def generate_llm_response(decision, entities, context, action_result):

    system_prompt = """
You are a professional e-commerce customer support assistant.
Use ONLY the provided facts.
Do NOT invent information.
If an error exists, politely explain it.
"""

    user_prompt = f"""
Action: {decision["action"]}
Tone: {decision["tone"]}
Facts: {action_result}

Generate a clear and helpful reply.
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.3,
        max_tokens=200
    )

    return response.choices[0].message.content.strip()
# ---------- Main Chat Endpoint ----------
@app.post("/chat")
def chat(req: ChatRequest):
    intent, confidence = intent_clf.predict(req.text)
    sentiment = sentiment_analyzer.analyze(req.text)
    entities = entity_extractor.extract(req.text)

    context = context_manager.get(req.user_id)

    decision = decision_layer.decide(
        intent=intent,
        confidence=confidence,
        sentiment=sentiment,
        entities=entities
    )

    action_result = action_executor.execute(
        decision=decision,
        entities=entities,
        context=context
    )

    reply = generate_llm_response(
        decision=decision,
        entities=entities,
        context=context,
        action_result=action_result
    )

    context_manager.update(req.user_id, {
        "last_intent": intent,
        "entities": entities
    })

    return {
        "reply": reply,
        "intent": intent,
        "decision": decision,
        "facts": action_result
    }