# 배열 합치기와 정렬
"""
Q. 배열 합치기와 정렬
설명:
    두개의 정수 배열 arr1 과 arr2 가 주어집니다.
    두 배열을 합친 후, 정렬하여 결과 배열을 반환하는 프로그램을 작성하세요.

요구사항:
    1. 두 배열을 합친 후, 선택한 정렬 알고리즘을 사용하여 정렬하세요
    2. 최종적으로 정렬된 배열을 반환합니다.

예시:
    입력: [1, 3, 5]
         [2, 4, 6]

    출력: [1, 2, 3, 4, 5, 6]

    입력: [10, 5, 15]
         [4, 11, 2]
    출력: [2, 4, 5, 10, 11, 15]
"""

# 두 배열을 합치고 정렬한다 == merge sort

def merge_sort(arr):
    if len(arr) <= 1: # item 이 하나 이하 시 정렬 완료
        return arr

    mid = len(arr) // 2 # median
    left_arr = merge_sort(arr[:mid]) # Sort
    right_arr = merge_sort(arr[mid:]) # Sort
    return merge(left_arr, right_arr)  # Merge

def merge(left, right):
    sorted_arr = []
    i = 0
    j = 0

    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            sorted_arr.append(left[i])
            i+=1
        else:
            sorted_arr.append(right[j])
            j+=1

    sorted_arr.extend(left[i:])
    sorted_arr.extend(right[j:])
    return sorted_arr

def merge_and_sort(arr1, arr2):
    merged_array = arr1 + arr2
    return merge_sort(merged_array)

# validator
arr1 = [1, 3, 5]
arr2 = [2, 4, 6]
assert merge_and_sort(arr1, arr2) == [1, 2, 3, 4, 5, 6]

arr1 = [10, 5, 15]
arr2 = [4, 11, 2]
assert merge_and_sort(arr1, arr2) == [2, 4, 5, 10, 11, 15]





