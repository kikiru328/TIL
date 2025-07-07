"""
Question:
1부터 N까지 차례대로 줄을 섰을 때, 맨 앞에 선 사람만 들여보내주고 그 다음 순서인 사람은
제일 뒤로 보내는 특이한 줄서기가 있습니다.

예를 들어, N=6인 경우, 123456 이 순서대로 줄을 서있을 것 입니다.
이때 제일 먼저 1이 입장하고 남은 순서는 23456이 됩니다.
2는 두 번째 순서이므로 제일 뒤로 보내서 34562가 됩니다.
다시 3이 입장하여 4562가 되고 4는 맨 뒤로 가게 되어 5624 순서가 됩니다.
이후 동일하게 5가 입장하여 624, 246이 되어 2가 입장,
46 -> 64가 되어 6이 입장 마지막으로 4가 입장하게 됩니다.

N이 주어질 때 제일 마지막으로 입장하는 숫자를 계산하는 프로그램을 작성하세요
"""
from collections import deque


def the_last_enter_number(number: int) -> int:
    deq = deque([i for i in range(1, number+1)])
    while len(deq) > 1: # deq 개수 1개 이상일 때
        deq.popleft() # enter first number
        first_after_enter = deq.popleft() # 2번째 숫자
        deq.append(first_after_enter) # 다시 뒤로

    return deq.pop() # 마지막 한개



assert the_last_enter_number(2) == 2
assert the_last_enter_number(3) == 2
assert the_last_enter_number(4) == 4
assert the_last_enter_number(5) == 2
assert the_last_enter_number(6) == 4
assert the_last_enter_number(7) == 6