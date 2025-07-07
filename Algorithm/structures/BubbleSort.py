def bubblesort(arr: list) -> list:
    # 첫 번째와 두번 째 비교,
    # n-1 만큼 반복된다.
    for i in range(len(arr) - 1):
        # 처음부터 마지막까지 두개씩 앞 뒤 비교, 작은 것이 뒤에 있으면 바꿈
        for j in range(len(arr) - 1 - i):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr


assert bubblesort([4, 6, 2, 9, 1]) == [1, 2, 4, 6, 9]
assert bubblesort([3, 2, 1, 5, 3, 2, 3]) == [1, 2, 2, 3, 3, 3, 5]