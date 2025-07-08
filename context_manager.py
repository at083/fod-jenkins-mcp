# minimal context manager for conversational state

class ContextManager:
    def __init__(self):
        self.sessions = {}

    def get_context(self, session_id):
        return self.sessions.get(session_id, {})

    def update_context(self, session_id, updates):
        ctx = self.sessions.get(session_id, {})
        ctx.update(updates)
        self.sessions[session_id] = ctx
        return ctx
