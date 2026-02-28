class DecisionLayer:
    def decide(self, intent, confidence, sentiment, entities):

        if intent == "fallback":
            return {"action": "clarify", "tone": "neutral"}

        if intent == "refund":
            return {
                "action": "refund_request",
                "requires_order_id": "ORDER_ID" not in entities,
                "tone": "apologetic" if sentiment["label"] == "NEGATIVE" else "polite"
            }

        if intent == "cancel_order":
            return {
                "action": "cancel_order",
                "requires_order_id": "ORDER_ID" not in entities,
                "tone": "polite"
            }

        if intent == "order_status":
            return {
                "action": "fetch_order_status",
                "requires_order_id": "ORDER_ID" not in entities,
                "tone": "apologetic" if sentiment["label"] == "NEGATIVE" else "neutral"
            }
        if intent == "shipping_issue":
            return {"action": "shipping_support", "tone": "apologetic"}

        if intent == "technical_issue":
            return {"action": "technical_support", "tone": "neutral"}

        return {"action": "general_support", "tone": "neutral"}