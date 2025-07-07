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

    def extract(self):
        if len(self.items) < 2: # 1이나 0이면
            return None

        root = self.items[1] # 최대값
        # Heap 규칙에 맞게 정리
        self.items[1], self.items[-1] = self.items[-1], self.items[1] #자리 변경
        self.items.pop() #최 하단 추출

        self._percolate_down(1)
        return root # 반환

    def _percolate_down(self, current_index):
        biggest_index = current_index # 가장 큰 값
        left_index = 2 * current_index #왼쪽 자식 노드
        right_index = 2 * current_index + 1 #오른쪽 자식 노드

        if left_index <= len(self.items) -1 and self.items[left_index] > self.items[right_index]:
            biggest_index = left_index
        if right_index <= len(self.items) -1 and self.items[right_index] > self.items[left_index]:
            biggest_index = right_index

        if biggest_index != current_index: # 큰 녀석이 부모가 아니다
            self.items[biggest_index], self.items[current_index] = self.items[current_index], self.items[biggest_index]
            self._percolate_down(biggest_index) # 재귀







