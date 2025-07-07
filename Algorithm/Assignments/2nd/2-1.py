# 후위 표기법 계산하기
"""
Q. 후위 표기법 계산하기
설명:
    후위 표기법(postfix notation)은 연산자가 피연산자 뒤에 오는 수식 표현 방식입니다.
    이 문제에서는 주어진 후위 표기법 수식을 계산하는 프로그램을 작성해야 합니다.

요구사항:
    1. 주어진 문자열은 공백으로 구분된 숫자와 사칙연산자(+,-,*,/)만을 포함합니다.
    2. 연산은 스택을 사용하여 수행해야 합니다.
    3. 연산의 결과는 정수로 반환합니다. 나눗셈의 경우 정수 나눗셈의 결과를 반환합니다.

예시:
    입력: 2 3 + 5 *
    출력: 25

    입력: 4 2 / 3 - 2 *
    출력: -2
"""

def postfix_notation_calculator(expression: str) -> int:
    stack: list = []
    symbols: str = '+-*/'
    # 계산이 되려면 두개의 숫자가 필요하다.
    for char in expression.split():
        if char.isdigit():
            stack.append(int(char))
        elif char in symbols:
            second_digit = stack.pop() #Stack: FILO
            first_digit = stack.pop()
            if char == '+':
                stack.append(first_digit + second_digit)
            elif char == '-':
                stack.append(first_digit - second_digit)
            elif char == '*':
                stack.append(first_digit * second_digit)
            else:
                stack.append(int(first_digit / second_digit)) # need to integer
    return stack.pop()

# test
insert_eg_1 = '2 3 + 5 *'
insert_eg_2 = '4 2 / 3 - 2 *'

assert postfix_notation_calculator(insert_eg_1) == 25, "Test 1 Failed"
assert postfix_notation_calculator(insert_eg_2) == -2, "Test 2 Failed"