---
created: 2025-02-28T14:55
updated: 2025-03-01T11:03
---
# 연결리스트
## Array vs Linked List

|        | Array                                                  | Linked List                                   |
| ------ | ------------------------------------------------------ | --------------------------------------------- |
| 구현     | List Type                                              | From Scratch                                  |
| 접근     | Easy                                                   | Hard                                          |
| 삽입     | Easy<br>- 데이터 추가 시 모든 공간이 다 차버렸다면, 새로운 메모리를 할당 받아야 한다. | Hard<br>- 모든 공간이 다 찼어도 맨 뒤의 노드만 동적으로 추가하면 된다. |
| 조회     | O(1)                                                   | O(N)                                          |
| 삭제(중간) | O(N)                                                   | O(1)                                          |
| 결론     | 데이터에 접근하는 경우가 빈번하다면 Array                              | 삽입과 삭제가 빈번하다면 Linked List                     |

```python
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
```