# 최장 증가 부분 수열(Longest Increasing Subsequence, LIS)
"""
Q. 최장 증가 부분 수열(Longest Increasing Subsequence, LIS)
설명:
    정수 배열이 주어졌을 때, 해당 배열 내에서 가장 긴 증가하는 부분 수열(LIS)의 길이를 찾는 프로그램을 작성하세요.
    부분 수열은 배열에서 몇몇 숫자를 제외한 순서가 유지된 수열을 의미합니다.

요구사항:
    1. 동적 계획법을 사용하여 문제를 해결합니다.
    2. 배열의 각 원소에 대해, 해당 원소를 마지막으로 하는 최장 증가 부분 수열의 길이를 계산합니다.
    3. 모든 가능한 부분 수열 중 최대 길이를 찾습니다

예시:
    입력: [10, 9, 2, 5, 3, 7, 101, 18]
    출력: 4
"""
def longest_increasing_subsequence(arr):
    if not arr:
        return 0  # 빈 배열이면 LIS 길이는 0

    n = len(arr)
    dp = [1] * n  # 각 원소를 마지막 원소로 하는 LIS 길이를 저장하는 DP 배열


    for i in range(1, n):
        for j in range(i):
            if arr[j] < arr[i]:  # 증가하는 관계인 경우
                dp[i] = max(dp[i], dp[j] + 1)  # 최댓값 갱신

    return max(dp)  # LIS의 최댓값 반환

# 테스트 예제
arr1 = [10, 9, 2, 5, 3, 7, 101, 18]
assert longest_increasing_subsequence(arr1) == 4

arr2 = [0, 1, 0, 3, 2, 3]
assert longest_increasing_subsequence(arr1) == 4

print("Success")