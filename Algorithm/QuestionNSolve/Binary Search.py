"""
Question:
오름차순으로 정렬된 정수 배열 nums와 정수 target이 주어졌을 때, nums에서 대상을 검색하는 함수를 작성합니다. 대상이 존재하면 그 색인을 반환합니다. 그렇지 않으면 -1을 반환합니다.

시간복잡도가 O(log n)인 알고리즘을 작성해야 합니다.

ex)
input: nums = [-1, 0, 3, 5, 9, 12], target = 9
Output: 4
"""

def binary_search(nums: list, target: int) -> int:
    # 반복되는 것은 재귀함수를 쓰는 경우가 많다.

    def bs(start, end): # 시작점과 끝점
        if start > end: # 내가 원하는게 없는 경우
            return -1 #없음

        mid = (start + end) // 2 #중앙값
        if nums[mid] == target:
            return mid
        elif nums[mid] > target:
            return bs(start, mid -1) # mid는 아니니까 그 전에
        elif nums[mid] < target:
            return bs(mid + 1, end) # mid는 아니니까 그 이후로

    return bs(0, len(nums)-1)



assert binary_search(nums=[-1, 0, 3, 5, 9, 12], target=9) == 4
assert binary_search(nums=[-1, 0, 3, 5, 9, 12], target=2) == -1