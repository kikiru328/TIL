# 미로 탈출 경로 찾기

## 튜터님에게 질문:
"""
이러한 문제를 보고 어떻게 BFS를 추론해야하는지, 어떤 방식으로 문제를 풀어나가야 하는지 궁금합니다.
"""



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

# BFS: 너비 우선 탐색. Queue를 사용한다.
# 상하좌우를 방문하는 것을 염두해둬야 한다.
# 미로의 (0,0)에서 시작한다.
# 상하좌우를 이동하면서 1이면 경로 길이의 1을 추가한다.
# 만약 다음 이동이 가능한 곳이 (N-1, M-1)일 경우 경로 길이에 1을 추가하고 종료.
# 방문시 해당 경로를 다시 가지 않는다: 최단거리

def escape_maze(maze) -> int:
# 우선 maze를 만든다
    rows = len(maze)
    columns = len(maze[0])

    # 상하좌우 움직이는 컨트롤러
    direction_rows = [0, 0, 1, -1] # 상하
    direction_columns = [1, -1, 0, 0] # 좌우

    # 방문
    visited = [[False] * columns for _ in range(rows)]

    # 시작 경로에서 움직이는 것이 중요.
    deq = deque()
    visited[0][0] = True # 시작경로 움직임
    deq.append((0, 0, 1)) # row, column, "move count"

    while deq: #maze에서 빠져나가기 전 까지
        # 상하좌우를 움직여보자
        current_row, current_column, move_count = deq.popleft()

        if current_row == rows - 1 and current_column == columns - 1: #exit
            return move_count

        for i in range(4):
            new_row = current_row + direction_rows[i]
            new_column = current_column + direction_columns[i]

            if 0 <= new_row < rows and 0 <= new_column < columns:
                if (maze[new_row][new_column] == '1'
                    and visited[new_row][new_column] == False): # 방문도 안했고, 1이면
                    visited[new_row][new_column] = True # 방문
                    deq.append((new_row, new_column, move_count+1))

assert escape_maze(maze=[["1", "1", "1", "0", "1"],
                         ["1", "0", "1", "0", "1"],
                         ["1", "0", "1", "0", "1"],
                         ["1", "1", "1", "1", "1"]]) == 8

assert escape_maze(maze=[["1", "1", "1", "1", "1"],
                         ["0", "0", "0", "0", "1"],
                         ["1", "1", "1", "0", "1"],
                         ["1", "0", "0", "0", "1"],
                         ["1", "1", "1", "1", "1"]]) == 9
