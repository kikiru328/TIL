# 최장 증가 부분 수열(Longest Increasing Subsequence, LIS)
"""
Q. 최장 증가 부분 수열(Longest Increasing Subsequence, LIS)
설명:
    정수 배열이 주어졌을 때, 해당 배열 내에서 가장 긴 증가하는 부분 수열(LIS)의 길이를 찾는 프로그램을 작성하세요.
    부분 수열은 배열에서 몇몇 숫자를 제외한 순서가 유지된 수열을 의미합니다.

요구사항:
    1. 동적 계획법을 사용하여 문제를 해결합니다.
    2. 배열의 각 원소에 대해, 해당 원소를 마지막으로 하는 최장 증가 부분 수열의 길이를 계산합니다.
    3. 모든 가능한 부분 수열 중 최대 길이를 찾습니다

예시:
    입력: 4
         5
         1 2 4
         1 3 2
         2 3 5
         2 4 1
         3 4 7
         1 4
    출력: 5
"""
import heapq
import sys

def dijkstra(n, roads, start, end):
    # 그래프 초기화 (인접 리스트)
    graph = {i: [] for i in range(1, n+1)}
    for u, v, cost in roads:
        graph[u].append((cost, v))
        graph[v].append((cost, u))  # 양방향 도로이므로 양쪽 추가

    # 최단 거리 배열 초기화
    INF = sys.maxsize
    distance = {i: INF for i in range(1, n+1)}
    distance[start] = 0  # 출발 도시의 거리는 0

    # 우선순위 큐 (최소 힙)
    pq = [(0, start)]  # (현재까지의 비용, 도시)

    while pq:
        curr_cost, curr_city = heapq.heappop(pq)

        # 현재 비용이 이미 저장된 거리보다 크다면 스킵
        if curr_cost > distance[curr_city]:
            continue

        # 인접한 도시 탐색
        for next_cost, next_city in graph[curr_city]:
            new_cost = curr_cost + next_cost
            if new_cost < distance[next_city]:  # 더 작은 비용이면 업데이트
                distance[next_city] = new_cost
                heapq.heappush(pq, (new_cost, next_city))

    return distance[end]  # 최종적으로 도착 도시까지의 최소 비용 반환

# 입력 예제
n = 4  # 도시 개수
m = 5  # 도로 개수
roads = [
    (1, 2, 4),
    (1, 3, 2),
    (2, 3, 5),
    (2, 4, 1),
    (3, 4, 7)
]
start_city, end_city = 1, 4  # 출발 도시와 도착 도시

# 최소 비용 계산
assert dijkstra(n, roads, start_city, end_city) == 5
print("Success")
