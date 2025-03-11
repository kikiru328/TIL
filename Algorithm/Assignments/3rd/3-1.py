# 미로 탈출 경로 찾기
"""
Q. 미로 탈출 경로 찾기
설명:
    N x M 크기의 미로가 주어집니다. 미로는 0과 1로 구성되어 있으며, 0은 이동할 수 없는 벽을
    나타내고, 1은 이동할 수 있는 경로를 나타냅니다.
    시작위치는 (0,0)이며, 미로의 출구는 (N-1, M-1)에 위치해있습니다.
    최단 경로로 미로를 탈출하는 방법을 찾는 프로그램을 작성하세요. 이동은 상하좌우로만 가능합니다.

요구사항:
    1. BFS 알고리즘을 사용하여 미로의 모든 경로를 탐색합니다.
    2. 시작 위치에서 출구까지의 최단 경로의 길이를 찾아야 합니다.
    3. 최단 경로의 길이를 반환합니다.
예시:
    입력: [
        ["1", "1", "1", "0", "1"],
        ["1", "0", "1", "0", "1"],
        ["1", "0", "1", "0", "1"],
        ["1", "1", "1", "1", "1"],
        ]                     X
    출력: 8 (0,0) -> (3, 4)

    입력:
        [
         ["1", "1", "1", "1", "1"],
         ["0", "0", "0", "0", "1"],
         ["1", "1", "1", "0", "1"],
         ["1", "0", "0", "0", "1"],
         ["1", "1", "1", "1", "1"],
         ]                     X
    출력: 9 (0,0) -> (4, 4)
"""
from collections import deque

maze = [
    ["1", "1", "1", "0", "1"],
    ["1", "0", "1", "0", "1"],
    ["1", "0", "1", "0", "1"],
    ["1", "1", "1", "1", "1"],
]
# BFS: 너비 우선 탐색. Queue를 사용한다.
# 상하좌우를 방문하는 것을 염두해둬야 한다.
# 미로의 (0,0)에서 시작한다.
# 상하좌우를 이동하면서 1이면 경로 길이의 1을 추가한다.
# 만약 다음 이동이 가능한 곳이 (N-1, M-1)일 경우 경로 길이에 1을 추가하고 종료.

# 우선 maze를 만든다
rows = len(maze)
columns = len(maze[0])

# 상하좌우 움직이는 컨트롤러
direction_rows = [0, 0, 1, -1] # 상하
direction_columns = [1, -1, 0, 0] # 좌우

# 이동 경로
move_count = 0


# 행과 열로 움직이게 함
for row in range(rows):
    for column in range(columns):
        if maze[row][column] != "1": # 0일 경우
            continue

        else: # 1일 경우
            move_count += 1 # 이동 + 1
            deq = deque() # direction
            deq.append((row, column)) # 시작단계

            while deq: # maze가 끝날때 까지
                current_row, current_column = deq.popleft() #현재 위치
                for i in range(4): # 상하좌우
                    new_row = current_row + direction_rows[i]
                    new_column = current_column + direction_columns[i]

                    if (new_row < 0 or new_row >= rows # maze 바깥
                        or new_column < 0 or new_column >= columns # maze 바깥
                        or maze[new_row][new_column] != '1'): # 안인데 1이 아닐경우, 갈 수 없을 경우
                        continue
                    else: # maze 안 이면서 1인 경우, 움직일 수 있는 경우
                        maze[new_row][new_column] = '0' # 방문 했고, 0으로 바꾼다.
                        deq.append((new_row,new_column))

print(move_count)

