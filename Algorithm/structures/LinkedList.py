# Linked List: Nodes Connected by Edges/arc

class ListNode:
    def __init__(self, value=0, next=None):
        self.value = value # node value
        self.next = next # edge/arc direction

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, value):
        if not self.head: # no head
            self.head = ListNode(value=value, next=None) # no data
            return
        node = self.head
        while node.next: # change node to next node
            node = node.next

        node.next = ListNode(value=value, next=None) # insert data to Node

Ll = LinkedList()
Ll.append(3)
Ll.append(5)
Ll.append(7)

print(Ll)

