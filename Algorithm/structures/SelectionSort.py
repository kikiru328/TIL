def selectionsort(lst: list) -> list:
    iters = len(lst) -1
    for iter in range(iters): # 요소 -1 씩 돌아갔을 때
        minimum = iter # 가장 작은 index라고 가정하고
        for current_index in range(iter+1, len(lst)):
            if lst[current_index] < lst[minimum]: #현재가 더 작다면
                minimum = current_index # 최소를 변경
        if minimum != iter: # 만약 최소값이 현재 index(초기)가 아니라면
            lst[minimum], lst[iter] = lst[iter], lst[minimum] #최소값과 현재의 index 위치 값을 변경
    return lst

assert selectionsort([4, 6, 2, 9, 1]) == [1, 2, 4, 6, 9]
assert selectionsort([3, 2, 1, 5, 3, 2, 3]) == [1, 2, 2, 3, 3, 3, 5]
