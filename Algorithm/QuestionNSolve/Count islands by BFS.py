"""
Question:
육지(1)과 물(0)으로 구성된 지도를 나타내는 m x n 크기의 이진 격자가 주어질 때,
섬의 개수를 반환합니다.
섬은 물로 둘러싸여 있으며, 인접한 육지를 가로 또는 세로로 연결하여 형성됩니다.

e.g 1)
Input: grid = [
    ["1", "1", "1", "1", "0"],
    ["1", "1", "0", "1", "0"],
    ["1", "1", "0", "0", "0"],
    ["0", "0", "0", "0", "0"],
]
Output: 1

e.g 2)
Input: grid = [
    ["1", "1", "0", "0", "0"],
    ["1", "1", "0", "0", "0"],
    ["0", "0", "1", "0", "0"],
    ["0", "0", "0", "1", "0"],
]
Output: 3
"""
from collections import deque

def island_bfs(grid):
    count_island = 0
    rows = len(grid)
    columns = len(grid[0])
    dr = [0, 0, 1, -1]
    dc = [1, -1, 0, 0]

    for row in range(rows):
        for column in range(columns):
            if grid[row][column] != '1':
                continue

            count_island += 1

            deq = deque([(row, column)])

            while deq:
                cur_r, cur_c = deq.popleft()
                for i in range(4):
                    nr = cur_r + dr[i]
                    nc = cur_c + dc[i]
                    if nr < 0 or nr >= rows or nc < 0 or nc >= columns or grid[nr][nc] != '1':
                        continue

                    grid[nr][nc] = '0' #방문
                    deq.append((nr, nc))
    return count_island

assert island_bfs(grid=[
    ["1", "1", "1", "1", "0"],
    ["1", "1", "0", "1", "0"],
    ["1", "1", "0", "0", "0"],
    ["0", "0", "0", "0", "0"]
]) == 1
assert island_bfs(grid=[
    ["1", "1", "0", "0", "0"],
    ["1", "1", "0", "0", "0"],
    ["0", "0", "1", "0", "0"],
    ["0", "0", "0", "1", "1"]
]) == 3