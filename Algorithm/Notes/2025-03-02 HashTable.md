---
created: 2025-03-02T00:46
updated: 2025-03-02T11:30
---
# 해시테이블
> 해시 함수를 이용해 Key를 값에 매핑하는 자료 구조


## 해시함수
1. 해시 함수란 임의 크기 데이터를 고정 크기 값으로 매핑하는데 사용할 수 있는 함수
2. 임의의 값을 넣어도 예상 크기 내에서 결과가 나오는 함수 (범위가 정해져있다)
3. eg:
```python
def modTree(n):
	return n%3
print(modTree(n)) # 0~3
```
*따라서 어떠한 값을 넣든 예측 값이 범위내에서 나오는 함수*

## 충돌
예측가능한 범위내에서 짝지어지는 구조이기 때문에 중복되는 경우가 있다 (value에 key가 2개)

> Chaining: 충돌 발생 시 연결 해가는 것 (계속 값을 저장: Linked List)
> Open Addressing: 탐색을 통해 빈 공간을 찾아나서는 방식

# Why?
충돌만 안난다면 O(1)으로 사용이 가능하기 때문.
# 구현
```python
class HashNode:  
    # save key & value, pointer  
    def __init__(self, key, value):  
        self.key = key  
        self.value = value  
        self.next = None  
  
  
class HashTable:  
    def __init__(self):  
        self.size = 10 # 사이즈 제한  
        self.table = [None] * self.size #10개 노드  
  
    def _hash_function(self, key):  
        return key % self.size # custom hash function  
  
    def put(self, key, value):  
        ind = self._hash_function(key) #result 0~9  
        if self.table[ind] is None: # 한 번도 결과값이 넣어지지 않은 경우  
            self.table[ind] = HashNode(key, value)  
        else: # 하나 이상의 결과값이 들어가있는 경우  
            node = self.table[ind]  
            while node.next is not None: # 다음 node가 있다면 변경  
                node = node.next  
            node.next = HashNode(key, value)  
  
  
    def get(self, key):  
        ind = self._hash_function(key)  
        node = self.table[ind]  
  
        while node is not None:  
            if node.key == key:  
                return node.value  
            node = node.next  
        return -1  
  
    def remove(self, key):  
        ind = self._hash_function(key)  
        node = self.table[ind]  
        prev_node = None # 이전 노드 기록  
  
        while node is not None:  
            if node.key == key:  
                if prev_node is None:  
                    self.table[ind] = node.next  
                else:  
                    prev_node.next = node.next # 지속적으로 동적  
                return  
            prev_node = node  
            node = node.next
```
