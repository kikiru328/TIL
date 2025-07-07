# 순열 생성하기
"""
Q. 순열 생성하기
설명:
    주어진 정수 배열에서 모든 가능한 순열을 생성하는 프로그램을 작성하세요
    배열에는 중복된 숫자가 없다고 가정합니다.

요구사항:
    1. 주어진 배열의 모든 숫자를 사용하여 만들 수 있는 모든 순열을 출력합니다.
    2. 백트래킹 알고리즘을 사용하여 효율적으로 모든 가능성을 탐색합니다.
예시:
    입력: [1, 2, 3]
    출력: [1, 2, 3]
         [1, 3, 2]
         [2, 1, 3]
         [2, 3, 1]
         [3, 1, 2]
         [3, 2, 1]

    입력: [1, 2, 3, 4]
    출력: [1, 2, 3, 4]
         [1, 2, 4, 3]
         [1, 3, 2, 4]
         [1, 3, 4, 2]
         [1, 4, 2, 3]
         [1, 4, 3, 2]
         [2, 1, 3, 4]
         [2, 1, 4, 3]
         [2, 3, 1, 4]
         [2, 3, 4, 1]
         [2, 4, 1, 3]
         [2, 4, 3, 1]
         [3, 1, 2, 4]
         [3, 1, 4, 2]
         [3, 2, 1, 4]
         [3, 2, 4, 1]
         [3, 4, 1, 2]
         [3, 4, 2, 1]
         [4, 1, 2, 3]
         [4, 1, 3, 2]
         [4, 2, 1, 3]
         [4, 2, 3, 1]
         [4, 3, 1, 2]
         [4, 3, 2, 1]
"""

# 배열에는 중복된 숫자가 없다.
# 각 자리 별로 조합이 이루어진다.
# 1을 첫째, 2는 둘째, 3은 셋째, 4는 넷째 라면
# 1은 선택할 수 없게한다.
# 각 자리별로 백트레킹을 진행한다

"""
order      select         remain      permutation
1          1              [2, 3]      [1]
1-2        2              [3]         [1, 2]
1-2-1      3              []          [1, 2, 3] *
1-3        3              [2]         [1, 3]
1-3-1      2              []          [1, 3, 2] *
2          2              [1, 3]      [2]
2-2        1              [3]         [2, 1]
2-2-1      3              []          [2, 1, 3] *
2-3        3              [1]         [2, 3]
2-3-1      1              []          [2, 3, 1] *
3          3              [1, 2]      [3]
3-2        1              [2]         [3, 1]
3-2-1      2              []          [3, 1, 2] *
3-3        2              [1]         [3, 2]
3-3-1      1              []          [3, 2, 1] * 
"""

def backtrack(remaining, process, result):
    # process: 제일 초반엔 빈 리스트
    # end condition
    if not remaining: # 남은 것이 없다면
        result.append(process[:]) # 조합들을 추가
        return

    # 하나씩 선택하는 것
    for i in range(len(remaining)):
        number = remaining[i]

        process.append(number) # 조합 리스트에 숫자 하나 추가
        next_remaining = remaining[:i] + remaining[i+1:] # 사용한 것 제외

        backtrack(next_remaining, process, result) # 이전것도 여기서 빠져나옴!
        process.pop()


def generate_permutations(input_list: list):
    result = []
    backtrack(input_list, [], result)
    print(result)
    return result

# 실행
input_list = [1, 2, 3]
generate_permutations(input_list)
