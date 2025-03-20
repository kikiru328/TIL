# 회의실 배정 최적화
"""
Q. 회의실 배정 최적화
설명:
    한 개의 회의실이 있으며, 사용할 수 있는 시간대가 여러 개 주어집니다. 각 시간대는 시작 시간과 종료 시간으로 구성됩니다.
    회의실을 사용할 수 있는 최대 회의 수를 찾는 프로그램을 작성하세요.
    한 회의가 끝나는 것과 동시에 다음 회의가 시작될 수 있습니다. 단, 회의는 미리 정해진 시간에만 시작해야 합니다.

요구사항:
    1. 주어진 모든 회의 시간대를 종료 시간이 빠른 순으로 정렬합니다.
    2. 정렬된 회의 시간대를 순회하면서, 각 회의가 현재 선택된 회의와 겹치지 않는 경우에만 회의를 선택합니다.
    3. 선택된 회의의 최대 개수를 구합니다

예시:
    입력: [(0, 6), (1, 4), (3, 5), (3, 8), (5, 7), (8, 9)]
    출력: 3

    입력: [(1, 3), (2, 4), (5, 8), (6, 10), (8, 11), (10, 12)]
    출력: 3
"""
def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left_half = merge_sort(arr[:mid])
    right_half = merge_sort(arr[mid:])

    return merge(left_half, right_half)

def merge(left, right):

    sorted_arr = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i][1] < right[j][1]:  # 종료 시간이 작은 순서대로 정렬
            sorted_arr.append(left[i])
            i += 1
        else:
            sorted_arr.append(right[j])
            j += 1

    sorted_arr.extend(left[i:])
    sorted_arr.extend(right[j:])

    return sorted_arr

def max_meetings(meetings):
    sorted_meetings = merge_sort(meetings)  # 종료 시간 기준으로 정렬
    count = 0
    last_end_time = 0

    for start, end in sorted_meetings:
        if start >= last_end_time:
            count += 1
            last_end_time = end

    return count

# validation
meetings = [(0, 6), (1, 4), (3, 5), (3, 8), (5, 7), (8, 9)]
assert max_meetings(meetings) == 3
