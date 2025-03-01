class Node:
    def __init__(self, value=0, next=None):
        self.value = value
        self.next = next

class Stack:
    def __init__(self):
        self.top = None

    def push(self, value):
        self.top = Node(value, self.top)

    def pop(self):
        if not self.top:
            return None

        node = self.top
        self.top = node.next
        return node.val

    def is_empty(self):
        return self.top is None