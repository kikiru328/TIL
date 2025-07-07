"""
Question:
주어진 리스트가 팰린드롬인지 판별하는 프로그램을 작성하세요.

ex)
insert: [1, 2, 2, 1]
print: True

insert: [1, 2]
print: False
"""
from structures.LinkedList import LinkedList

linked_list = LinkedList()

l1 = LinkedList()
for num in [1, 2, 2, 1]: # 1 -> 2 -> 2 -> 1
    l1.append(num)

l2 = LinkedList()
for num in [1, 2]: # 1 -> 2
    l2.append(num)

def is_palindrome(ln) -> bool:
    arr = []
    head = ln.head

    if not head:
        return True

    node = head
    while node:
        arr.append(node.value)
        node = node.next

    while len(arr) > 1:
        first = arr.pop(0)
        last =arr.pop()
        if first != last:
            return False
    return True

assert is_palindrome(l1)
assert not is_palindrome(l2)