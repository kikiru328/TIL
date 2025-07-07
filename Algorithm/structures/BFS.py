# BFS
from collections import deque

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

def bfs_queue(graph, start_node):
    visited = []
    deq = deque([start_node])

    while deq:
        node = deq.popleft()
        visited.append(node)
        for adj in graph[node]:
            if adj not in visited:
                deq.append(adj)

    return visited

"""
BFS Flow
order   node   visited                                      Queue
1       1      [1]                                          [2, 5, 9]
2       2      [1, 2]                                       [5. 9, 1, 3]
3       5      [1, 2, 5]                                    [9, 1, 3, 1, 6, 8]
4       9      [1, 2, 5, 9]                                 [1, 3, 1, 6, 8, 1, 10]
5       1      visited                                      [3, 1, 6, 8, 1, 10]
6       3      [1, 2, 5, 9, 3]                              [1, 6, 8, 1, 10, 2, 4]
7       1      visited                                      [6, 8, 1, 10, 2, 4]
8       6      [1, 2, 5, 9, 3, 6]                           [8, 1, 10, 2, 4, 5, 7]
9       8      [1, 2, 5, 9, 3, 6, 8]                        [1, 10, 2, 4, 5, 7, 5]
10      1      visited                                      [10, 2, 4, 5, 7, 5]
11      10     [1, 2, 5, 9, 3, 6, 8, 10]                    [2, 4, 5, 7, 5, 9]
12      2      visited                                      [4, 5, 7, 5, 9]
13      4      [1, 2, 5, 9, 3, 6, 8, 10, 4]                 [5, 7, 5, 9, 3]
14      5      visited                                      [7, 5, 9, 3]
15      7      [1, 2, 5, 9, 3, 6, 8, 10, 4, 7]              [5, 9, 3]
16      5      visited                                      [9, 3]
17      9      visited                                      [3]
16      3      visited                                      []

return = [1, 2, 5, 9, 3, 6, 8, 10, 4, 7
"""

assert bfs_queue(graph, 1) == [1, 2, 5, 9, 3, 6, 8, 10, 4, 7]