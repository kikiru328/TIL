def insertionsort(lst: list) -> list:
    iters = len(lst) - 1 # 배열의 길이보다 하나 작은 값이 순환
    for iter in range(iters):
        for current_index in reversed(range(1, iter+2)): # 점차 작은 것으로 가니까, reversed
            # 또한 최소 1이어야 된다 (current-1이 -1이 되면 안된다)
            # iter=0일 경우, current index는 최소 1 이여야 한다 (current_index-1가 iter)
            if lst[current_index-1] > lst[current_index]: # 현재가 전에 있는 것 보다 작으면
                lst[current_index-1], lst[current_index] = lst[current_index], lst[current_index-1]
            else: # 이미 잘 정렬되어 있음
                break

    return lst



assert insertionsort([4, 6, 2, 9, 1]) == [1, 2, 4, 6, 9]
assert insertionsort([3, 2, 1, 5, 3, 2, 3]) == [1, 2, 2, 3, 3, 3, 5]