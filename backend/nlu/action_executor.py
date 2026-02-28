class ActionExecutor:
    def execute(self, decision, entities, context):
        action = decision["action"]

        # ---- MOCK ORDER DB ----
        MOCK_ORDER_DB = {
            "123456": {
                "status": "Out for delivery",
                "expected_delivery": "Today by 9 PM"
            },
            "998877": {
                "status": "Delivered",
                "delivered_on": "Yesterday"
            }
        }

        # ---- ORDER STATUS ----
        if action == "fetch_order_status":
            order_ids = entities.get("ORDER_ID", [])
            if not order_ids:
                return {"error": "ORDER_ID_MISSING"}

            order_id = order_ids[0]
            order = MOCK_ORDER_DB.get(order_id)

            if not order:
                return {"error": "ORDER_NOT_FOUND"}

            return {
                "order_id": order_id,
                "status": order["status"],
                **order
            }

        # ---- DEFAULT ----
        return {}