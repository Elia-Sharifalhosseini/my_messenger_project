class HashNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None

class HashTable:
    def __init__(self, capacity=10):
        self.capacity = capacity
        self.size = 0
        self.buckets = [None] * self.capacity

    def hash_function(self, key):
        return hash(key) % self.capacity

    def insert(self, key, value):
        index = self.hash_function(key)
        head = self.buckets[index]

        # Check if key already exists, update value
        while head:
            if head.key == key:
                head.value = value
                return
            head = head.next

        # Insert new node at the head of chain
        new_node = HashNode(key, value)
        new_node.next = self.buckets[index]
        self.buckets[index] = new_node
        self.size += 1

    def get(self, key):
        index = self.hash_function(key)
        head = self.buckets[index]
        while head:
            if head.key == key:
                return head.value
            head = head.next
        return None

    def delete(self, key):
        index = self.hash_function(key)
        head = self.buckets[index]
        prev = None
        while head:
            if head.key == key:
                if prev:
                    prev.next = head.next
                else:
                    self.buckets[index] = head.next
                self.size -= 1
                return True
            prev = head
            head = head.next
        return False

    def __str__(self):
        result = ""
        for i in range(self.capacity):
            result += f"Bucket {i}: "
            node = self.buckets[i]
            while node:
                result += f"({node.key}, {node.value}) -> "
                node = node.next
            result += "None\n"
        return result
