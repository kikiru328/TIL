class BinaryMaxHeap:
    def __init__(self):
        self.items = [None]

    def insert(self, key):
        self.items.append(key) # 마지막 노드에 값을 넣는다
        # 부모 노드와 비교해야 함

    def _percolate_up(self): #percolate: 스며들다
        current_index = len(self.items) - 1
        parent_index = current_index // 2 # 완전 이진 트리에서 부모의 인덱스는 2로 나눈 몫
        # [1, 2, 3] -> 배열 길이의 -1 이 나의 Index
        while parent_index > 0: # 최대가 아니라면
            if self.items[current_index] > self.items[parent_index]: #나의 값이 부모의 값보다 크다면
                self.items[current_index], self.items[parent_index] = self.items[parent_index], self.items[current_index] # 자리변경
                current_index = parent_index # index 변경
                parent_index = current_index // 2 # 강등 (index 변경)
                




