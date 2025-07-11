class Message:
    def __init__(self, id, sender, content, timestamp):
        self.id = id
        self.sender = sender
        self.content = content
        self.timestamp = timestamp
        self.replies = LinkedList()

class ReplyNode:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def add_reply(self, reply):
        new_node = ReplyNode(reply)
        new_node.next = self.head
        self.head = new_node

    def get_all_replies(self):
        replies = []
        current = self.head
        while current:
            replies.append(current.data)
            current = current.next
        return replies