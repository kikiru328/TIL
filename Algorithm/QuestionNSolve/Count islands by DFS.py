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


def island_dfs_stack(grid):
    # 상하좌우로 이동해야 함.
    # grid[row-1][column] 상
    # grid[row+1][column] 하
    # grid[row][column-1] 좌
    # grid[row][column+1] 우
    dr = [-1, 1, 0, 0] # 상 하
    dc = [0, 0, -1, 1] # 좌 우

    # 경계?
    rows = len(grid)
    columns = len(grid[0])

    # 섬의 개수
    count_island = 0

    for r in range(rows): # 각 줄을 돌면서
        for c in range(columns): # 그 줄 중 하나씩 돌면서
            if grid[r][c] != '1': # 1이 아니라면 반복
                continue
            # 1인 점 도달
            count_island += 1

            stack = [(r, c)] # 방문해야 할 노드들
            while stack:
                x, y = stack.pop()
                grid[x][y] = '0' # 더이상 이 노드를 신경쓰지 않는다.
                # 여기서 상하좌우를 살핀다.
                for i in range(4):
                    new_row = x + dr[i] #상하
                    new_column = y + dc[i] # 좌우

                    if (new_row < 0 or new_row >= rows # rows 범위 안에
                            or new_column < 0 or new_column >= columns # columns 범위 안에
                            or grid[new_row][new_column] != '1'): # 상하좌우에 1이 있다면 반복 (0으로 만들기)
                        continue

                    stack.append((new_row, new_column)) #

    return count_island

def island_dfs_recursive(grid):
    dx = [0, 0, 1, -1]
    dy = [1, -1, 0, 0]
    m = len(grid)
    n = len(grid[0])
    cnt = 0

    def dfs_recursive(r, c):
        if r < 0 or r >= m or c < 0 or c >= n or grid[r][c] != '1':
            return

        # 방문처리
        grid[r][c] = '0'
        for i in range(4):
            dfs_recursive(r + dx[i], c + dy[i])
        return

    for r in range(m):
        for c in range(n):
            node = grid[r][c]
            if node != '1':
                continue

            cnt += 1
            dfs_recursive(r, c)

    return cnt


assert island_dfs_recursive(grid=[
    ["1", "1", "1", "1", "0"],
    ["1", "1", "0", "1", "0"],
    ["1", "1", "0", "0", "0"],
    ["0", "0", "0", "0", "0"]
]) == 1
assert island_dfs_recursive(grid=[
    ["1", "1", "0", "0", "0"],
    ["1", "1", "0", "0", "0"],
    ["0", "0", "1", "0", "0"],
    ["0", "0", "0", "1", "1"]
]) == 3









assert island_dfs_stack(grid=[
    ["1", "1", "1", "1", "0"],
    ["1", "1", "0", "1", "0"],
    ["1", "1", "0", "0", "0"],
    ["0", "0", "0", "0", "0"]
]) == 1
assert island_dfs_stack(grid=[
    ["1", "1", "0", "0", "0"],
    ["1", "1", "0", "0", "0"],
    ["0", "0", "1", "0", "0"],
    ["0", "0", "0", "1", "1"]
]) == 3

assert island_dfs_recursive(grid=[
    ["1", "1", "1", "1", "0"],
    ["1", "1", "0", "1", "0"],
    ["1", "1", "0", "0", "0"],
    ["0", "0", "0", "0", "0"]
]) == 1
assert island_dfs_recursive(grid=[
    ["1", "1", "0", "0", "0"],
    ["1", "1", "0", "0", "0"],
    ["0", "0", "1", "0", "0"],
    ["0", "0", "0", "1", "1"]
]) == 3