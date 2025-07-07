class Node:
    def __init__(self, value=0, next=None):
        self.value = value
        self.next = next


class Queue:
    def __init__(self):
        self.front = None

    def push(self, value):
        if not self.front: # if empty
            self.front = Node(value)
            return # end

        node = self.front
        while node.next:
            node = node.next

        node.next = Node(value)

    def pop(self, value):
        if not self.front:
            return None
        node = self.front
        return node.value

    def is_empty(self, value):
        return self.front in None

