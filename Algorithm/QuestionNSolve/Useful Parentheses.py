"""
Question:
'(', ')', '{', '}', '[' 및 ']' 만 포함된 문자열이 주어졌을 때,
입력 문자열이 유효한지 확인하는 프로그램을 작성하세요

insert: '()'
print: True

insert: '(()))'
print: False
"""
def test_problem_stack(parentheses: str):
    stack = []
    pair = {
        ')': '(',
        '}': '{',
        ']': '['
    }
    for char in parentheses:
        if char in '({[': # open
            stack.append(char)
        else: # close
            if not stack: # empty
                return False

            top = stack.pop() #> pop close
            if pair[char] != top: #check pairs
                return False
    return not stack

assert test_problem_stack("()")
assert test_problem_stack("()[]{}")
assert test_problem_stack("({[][]})")
assert test_problem_stack("({[]})")
assert not test_problem_stack("(]")
assert not test_problem_stack("(()]")
assert not test_problem_stack("(((])")
assert not test_problem_stack("((())")

