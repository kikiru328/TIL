"""
Question:
N * N 체스판에 N 개의 퀸을 배치할 수 있는 경우의 수를 나열하는 문제.
퀸은 상하좌우, 대각선 방향으로 거리 제한 없이 이동할 수 있다.

*전형적인 backtracking 문제

ex)
insert: n = 4
print: [[".Q..", "...Q", "Q...", "..Q."], ["..Q.", "Q...", "...Q', ".Q.."]]

insert: n = 1
print: [["Q"]]
"""

def nqueen(n: int) -> list:
    answer = []
    checked = [-1] * n # 탐색되지 않은 상황을 -1 * column 개수

    # (1, n) 을 놓아야 했다면, 앞으로는 (1, n) 이 나올 수 없다.
    # checked[1] = 3 으로 사용하면 된다 (1행 3열)

    # 1. n개의 퀸을 순서대로 체스판에 두어야 한다. (경우의 수: BFS, DFS)
    # 2. 첫번째 퀸을 두고 조건에서 벗어나는 경우의 수는 제외한다. (경우의 수 제외: BackTracking)
    def is_ok(row): # 조건 검증
        for x in range(row):
            if (checked[x] == checked[row] # Column이 같지는 않은 지
                    or abs(x-row) == abs(checked[x]-checked[row])):# 대각선: 열값의 차이와 행값의 차이 (길이가) 동일
                # 조건 불 만족
                return False
        return True




    def dfs(row):
        # 행을 결정, 어디에 둘 것 인지
        if row >= n: # 모든 수를 완성할 때 까지
            result = [['.'] * n for _ in range(n)]# 체스판 생성
            for x in range(n):
                result[x][checked[x]] = "Q"
            answer.append([''.join(result[idx]) for idx in range(n)])
            return

        for column in range(n):
            checked[row] = column # r, c에 퀸이 놓여있다. 10번째 행에 뒀다는 것은 9번째까지 존재하는 수가 있고 조건에 맞음.
            if is_ok(row): # 조건 판단
                dfs(row+1) # recursive

    dfs(0)
    return answer

assert nqueen(4) == [[".Q..", "...Q", "Q...", "..Q."], ["..Q.", "Q...", "...Q", ".Q.."]]