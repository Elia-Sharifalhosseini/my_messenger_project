from data_structures.linked_list import LinkedList
import time

class Message:
    def __init__(self, message_id, sender_username, content, timestamp=None, replies=None):
        self.message_id = message_id
        self.sender_username = sender_username
        self.content = content
        self.timestamp = timestamp if timestamp else time.time()
        self.replies = replies if replies else LinkedList()

    def add_reply(self, reply_message):
        self.replies.add_reply(reply_message)

    def get_replies(self):
        return self.replies.get_all_replies()

    def to_dict(self):
        return {
            "message_id": self.message_id,
            "sender_username": self.sender_username,
            "content": self.content,
            "timestamp": self.timestamp,
            "replies": [r.to_dict() if isinstance(r, Message) else r for r in self.replies.get_all_replies()]
        }

    @staticmethod
    def from_dict(data):
        replies_list = LinkedList()
        for reply_data in data.get("replies", []):
            reply_msg = Message.from_dict(reply_data)
            replies_list.add_reply(reply_msg)
        return Message(
            data["message_id"],
            data["sender_username"],
            data["content"],
            data["timestamp"],
            replies_list
        )
