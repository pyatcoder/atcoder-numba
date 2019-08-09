# Educational DP Contest / DP まとめコンテスト
# 問題 J - Sushi
# https://atcoder.jp/contests/dp/tasks/dp_j
import numpy as np
from numba import njit

@njit
def solve(n1, n2, n3, N, dp):
    if dp[n1, n2, n3] >= 0:
        return dp[n1, n2, n3]
    if n1 == 0 and n2 == 0 and n3 == 0:
        return 0.0

    res = 0.0
    if n1 > 0:
        res += solve(n1 - 1, n2, n3, N, dp) * n1
    if n2 > 0:
        res += solve(n1 + 1, n2 - 1, n3, N, dp) * n2
    if n3 > 0:
        res += solve(n1, n2 + 1, n3 - 1, N, dp) * n3
    res += N
    res *= 1.0 / (n1 + n2 + n3)

    dp[n1, n2, n3] = res
    return res


N = int(input())
n1 = 0
n2 = 0
n3 = 0
for s in input().split():
    if s == '1':
        n1 += 1
    elif s == '2':
        n2 += 1
    else:
        n3 += 1
dp = np.full((N + 1, N + 1, N + 1), -1.)
solve(n1, n2, n3, N, dp)
print(dp[n1, n2, n3])

