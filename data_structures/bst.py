class BSTNode:
    def __init__(self, key, message):
        self.key = key  # مثلاً ID پیام
        self.message = message
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None

    def insert(self, key, message):
        self.root = self._insert(self.root, key, message)

    def _insert(self, node, key, message):
        if node is None:
            return BSTNode(key, message)
        if key < node.key:
            node.left = self._insert(node.left, key, message)
        else:
            node.right = self._insert(node.right, key, message)
        return node

    def search(self, key):
        return self._search(self.root, key)

    def _search(self, node, key):
        if node is None or node.key == key:
            return node
        if key < node.key:
            return self._search(node.left, key)
        else:
            return self._search(node.right, key)

    def delete(self, key):
        self.root = self._delete(self.root, key)

    def _delete(self, node, key):
        if node is None:
            return node
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            # پیدا کردن کوچکترین مقدار در سمت راست
            temp = self._min_value_node(node.right)
            node.key = temp.key
            node.message = temp.message
            node.right = self._delete(node.right, temp.key)
        return node

    def _min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def inorder(self):
        messages = []
        self._inorder(self.root, messages)
        return messages

    def _inorder(self, node, messages):
        if node:
            self._inorder(node.left, messages)
            messages.append(node.message)
            self._inorder(node.right, messages)