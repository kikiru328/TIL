"""
Question:
그래프를 DFS로 탐색한 결과와 BFS로 탐색한 결과를 출력하는 프로그램을 작성하시오.
단, 방문할 수 있는 정점이 여러 개인 경우에는 정점 번호가 작은 것을 먼저 방문하고,
더 이상 방문할 수 있는 점이 없는 경우 종료한다. 정점 번호는 1번부터 N번까지이다.

insert:
첫째 줄에 정점의 개수 N(1 ≤ N ≤ 1,000), 간선의 개수 M(1 ≤ M ≤ 10,000),
탐색을 시작할 정점의 번호 V가 주어진다.
다음 M개의 줄에는 간선이 연결하는 두 정점의 번호가 주어진다.
어떤 두 정점 사이에 여러 개의 간선이 있을 수 있다. 입력으로 주어지는 간선은 양방향이다.

print:
첫째 줄에 DFS를 수행한 결과를, 그 다음 줄에는 BFS를 수행한 결과를 출력한다.
V부터 방문된 점을 순서대로 출력하면 된다.

ex)
insert:
4 5 1
1 2
1 3
1 4
2 4
3 4

print:
1 2 4 3
1 2 3 4
"""

# 모든 문제를 풀때, 3가지를 정리하고 시작한다.
# 입력: N, M, V -> 정점 개수, 간선 개수, 시장 정점
#      다음 M개 줄에 걸쳐 간선 정보를 줌 (간선 리스트<-)
N, M, V = map(int, input().split())


# 로직:
#       주어진 간선 리스트를 BFS/DFS 하기 편한 형태의 자료 구조로 바꾸고
#           간선 리스트 -> 인접 행렬
graph = [[0] * (N+1) for _ in range(N+1)] #index mapping
for _ in range(M):
    a, b = map(int, input().split())
    graph[a][b] = graph[b][a] = 1 # 간선, # 양방향 그래프


#       DFS 함수 구현
visited_dfs = [0] * (N+1) # 0: 미방문 / 1: 방문
def dfs(V): # 시작 간선
    stack = [V]

    result = []

    while stack:
        node = stack.pop()
        if visited_dfs[node] == 0:
            visited_dfs[node] = 1
            result.append(node)

            for i in range(N, 0, -1): # 역순
                    if graph[node][i] == 1 and visited_dfs[i] == 0:
                        stack.append(i)

    # 출력: DFS 로 탐색했을 때 탐색 노드 순서 출력
    return result

#       BFS 함수 구현
visited_bfs = [0] * (N+1)
def bfs(V): # 시작 간선
    queue = [V]
    result = []
    visited_bfs[V] = 1\

    while queue:
        node = queue.pop(0)
        result.append(node)

        for i in range(1, N+1):
            if graph[node][i] == 1 and visited_bfs[i] == 0:
                queue.append(i)
                visited_bfs[i] = 1
    # 출력: BFS 로 탐색했을 때 탐색 노드 순서 출력
    return result

# 출력하기
print(*dfs(V))
print(*bfs(V))
