# 중복 문자 없는 가장 긴 부분 문자열 찾기
"""
Q. 중복 문자 없는 가장 긴 부분 문자열 찾기
설명:
    주어진 문자열에서 중복 문자가 없는 가장 긴 부분 문자열의 길이를 찾는 문제입니다.
    이 문제를 해결하기 위해 해시테이블을 사용하여 문자의 위치를 추적합니다.
요구사항:
    1. 문자열에 포함된 모든 문자에 대해 최근 위치를 저장하는 해시테이블을 사용합니다.
    2. 중복된 문자가 발견될 때, 부분 문자열의 시작 위치를 업데이트합니다.
    3. 중복되지 않는 가장 긴 부분 문자열의 최대 길이를 반환합니다.

예시:
    입력: abcabcbb
    출력: 3

    입력: bbbbb
    출력: 1
"""

"""
abcabcbb
idea
 1 문자를 하나씩 돌아가면서 추출한다.
 2 앞으로 나올 문자가 중복되는지 안되는지를 판단하기 좋은 자료구조는 dict --> hash table을 이용한다.
 3 문자를 key, index를 value로 hash_table에 추가한다.
 4 문자가 중복되지 않으면 start index는 변환이 없다. 대신 max_length는 갱신된다.
    max_length의 갱신은 
        현재의 max_length와 start index에서 현재 char index까지의 길이 +1 
        (initial index = 0) 중 큰 값.
 5 문자가 중복된다면 최초 시작 index를 포함한 문자가 hash table에 있다는 뜻 이기에 
    start는 이전 중복된 char index 에 1을 +하고, hash_table에 존재하는 char의 value 또한 변경된다.
 6 이를 반복 후, 반복문이 종료되었을때 max_length를 반환한다.
 
blue print
 word: 'abcabcbb'
 start index/ char/ index/ hash_table {char/index} / current_word/ max_length
 0             a      0   {"a": 0}                   a               1
 0             b      1   {"a": 0, "b": 1}           ab              2
 0             c      2   {"a": 0, "b": 1, "c": 2}   abc             3
 1 "a" 0+1     a      3   {"a": *3, "b": 1, "c": 2}  bca             3
 2 "b" 1+1     b      4   {"a": 3, "b": *4, "c": 2}  cab             3
 3 "c" 2+1     c      5   {"a": 3, "b": 4, "c": *5}  abc             3
 5 "b" 4+1     b      6   {"a": 3, "b": *6, "c": 5}  cb              3
 7 "b" 6+1     b      7   {"a": 3, "b": *7, "c": 5}  b               3
 
 return 3
"""
def length_of_longest_word(word: str) -> int:
    hash_table: dict = {}
    start_index: int = 0
    max_length: int = 0
    for current_index, char in enumerate(word):
        # 중복일경우 혹은 바로 같은 문자가 나왔을 경우
        if char in hash_table and hash_table[char] >= start_index:
            start_index = current_index + 1
        hash_table[char] = current_index
        max_length = max(max_length, current_index-start_index+1)
    return max_length

assert length_of_longest_word('abcabcbb') == 3
assert length_of_longest_word('bbbbb') == 1