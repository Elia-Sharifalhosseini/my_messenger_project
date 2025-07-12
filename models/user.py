class User:
    def __init__(self, username, display_name=None):
        self.username = username
        self.display_name = display_name if display_name else username
        self.messages_sent = []  # مثلا لیستی از message_id ها یا Message ها

    def add_message(self, message_id):
        self.messages_sent.append(message_id)

    def __str__(self):
        return f"User(Username={self.username}, DisplayName={self.display_name}, MessagesSent={self.messages_sent})"
