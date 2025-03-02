# chaining
# moduler calculation
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


# Test
ht = HashTable()

ht.put(1, 1)
ht.put(2, 2)
assert ht.get(1) == 1
assert ht.get(2) == 2
assert ht.get(3) == -1

ht.put(12, 1)
ht.put(22, 2)
ht.put(32, 3)
assert ht.get(12) == 1
assert ht.get(22) == 2
assert ht.get(32) == 3

ht.remove(12)
assert ht.get(2) == 2
assert ht.get(12) == -1
assert ht.get(22) == 2
assert ht.get(32) == 3

ht.get(2)