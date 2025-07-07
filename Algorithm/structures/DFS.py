# DFS recursive
from html.parser import starttagopen


def dfs_recursive(graph: dict, node: int, visited: list):
    # 방문 기록
    visited.append(node)

    for adj in graph[node]: # 그래프에서 인접 노드에서
        if adj not in visited: # 방문한 적이 없다면
            dfs_recursive(graph, adj, visited) # 해당 인접 노드에서 다시 시작

    return visited

# DFS Stack
def dfs_stack(graph: dict, start: int):
    visited = [] #방문한 경로
    stack = [start] # 방문해야 하는 노드의 목록

    while stack:
        node = stack.pop()
        visited.append(node)

        for adj in graph[node]:
            if adj not in visited:
                stack.append(adj)

    return visited

"""dfs stack
order   node   visited                                      stack
1        1     [1]                                          [2, 5, 9]
2        9     [1, 9]                                       [2, 5, 1, 10]
3       10     [1, 9, 10]                                   [2, 5, 1, 10, 9]
4        9     visited                                      [2, 5, 1, 10]
5       10     visited                                      [2, 5, 1]
6        1     visited                                      [2, 5]
7        5     [1, 9, 10, 5]                                [2, 1, 6, 8]
8        8     [1, 9, 10, 5, 8]                             [2, 1, 6, 5]
9        5     visited                                      [2, 1, 6]
10       6     [1, 9, 10, 5, 8, 6]                          [2, 1, 5, 7]
11       7     [1, 9, 10, 5, 8, 6, 7]                       [2, 1, 5, 6]
12       6     visited                                      [2, 1, 5]
13       5     visited                                      [2, 1]
14       1     visited                                      [2]
15       2     [1, 9, 10, 5, 8, 6, 7, 2]                    [1, 3]
16       3     [1, 9, 10, 5, 8, 6, 7, 2, 3]                 [1, 2, 4]
17       4     [1, 9, 10, 5, 8, 6, 7, 2, 3, 4]              [1, 2]
18       2     visited                                      [1]
19       1     visited                                      []
>>> visited = [1, 9, 10, 5, 8, 6, 7, 2, 3, 4]
"""



graph = {
    1: [2, 5, 9],
    2: [1, 3],
    3: [2, 4],
    4: [3],
    5: [1, 6, 8],
    6: [5, 7],
    7: [6],
    8: [5],
    9: [1, 10],
    10: [9]
}

assert dfs_recursive(graph, 1, []) == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
assert dfs_stack(graph, 1) == [1, 9, 10, 5, 8, 6, 7, 2, 3, 4]

