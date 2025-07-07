def merge(arr1, arr2):
    result = []
    i = 0
    j = 0

    while i < len(arr1) and j < len(arr2): # valid
        if arr1[i] < arr2[j]:
            result.append(arr1[i])
            i += 1
        else:
            result.append(arr2[j])
            j += 1

    for idx in range(i, len(arr1)):
        result.append(arr1[idx])

    for idx in range(j, len(arr2)):
        result.append(arr2[idx])

    return result

assert merge([1,2,3,5],[4,6,7,8]) == [1,2,3,4,5,6,7,8]


def mergesort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = arr[:mid]
    right = arr[mid:]
    return merge(mergesort(left), mergesort(right))

assert mergesort([4, 6, 2, 9, 1]) == [1, 2, 4, 6, 9]
assert mergesort([3, 2, 1, 5, 3, 2, 3]) == [1, 2, 2, 3, 3, 3, 5]