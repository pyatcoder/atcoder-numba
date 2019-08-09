import numpy as np
from numba import njit

@njit
def solve(dp, N):
    for l in range(1, N + 1):
        for i in range(l, -1, -1):
            for j in range(l - i, -1, -1):
                k = l - i - j

                ALLSum = 0
                AllP = (i + j + k) / N
                Loop = 1 / AllP

                if i != 0:
                    ALLSum += dp[i - 1, j, k] * i / N
                if j != 0:
                    ALLSum += dp[i + 1, j - 1, k] * j / N
                if k != 0:
                    ALLSum += dp[i, j + 1, k - 1] * k / N

                dp[i, j, k] = ALLSum / AllP + Loop


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
dp = np.zeros((N + 1, N + 1, N + 1))
solve(dp, N)
print(dp[n1, n2, n3])
