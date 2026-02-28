class ContextManager:
    def __init__(self):
        self.sessions = {}

    def update(self, user_id, data):
        if user_id not in self.sessions:
            self.sessions[user_id] = {}

        self.sessions[user_id].update(data)

    def get(self, user_id):
        return self.sessions.get(user_id, {})