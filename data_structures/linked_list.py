class ListNode:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def add_reply(self, data):
        new_node = ListNode(data)
        if not self.head:
            self.head = new_node
            return
        # Add at end
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node

    def get_all_replies(self):
        replies = []
        current = self.head
        while current:
            replies.append(current.data)
            current = current.next
        return replies

    def __str__(self):
        result = ""
        current = self.head
        while current:
            result += f"{current.data} -> "
            current = current.next
        result += "None"
        return result
