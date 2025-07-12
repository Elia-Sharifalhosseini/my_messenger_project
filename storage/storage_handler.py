import json
import os
from models.message import Message

class StorageHandler:
    def __init__(self, file_path='data.json'):
        self.file_path = file_path
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as f:
                json.dump({"users": {}, "messages": {}}, f)

    def load_data(self):
        with open(self.file_path, 'r') as f:
            data = json.load(f)
        return data

    def save_data(self, data):
        with open(self.file_path, 'w') as f:
            json.dump(data, f, indent=4)

    def save_user(self, username, user_data):
        data = self.load_data()
        data["users"][username] = user_data
        self.save_data(data)

    def save_message(self, message):
        data = self.load_data()
        data["messages"][str(message.message_id)] = message.to_dict()
        self.save_data(data)

    def get_user(self, username):
        return self.load_data()["users"].get(username, None)

    def get_all_messages(self):
        messages_dict = self.load_data()["messages"]
        return {int(k): Message.from_dict(v) for k, v in messages_dict.items()}

    def get_next_message_id(self):
        all_messages = self.load_data()["messages"]
        return len(all_messages) + 1
