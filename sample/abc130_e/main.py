import sys
import numpy as np
from numba import njit
input = sys.stdin.buffer.readline

@njit('(u4[:,:],u4[:],u4[:])')
def calc(a, S, T):
    MOD = 10 ** 9 + 7
    for i in range(1, a.shape[0]):
        for j in range(1, a.shape[1]):
            a[i, j] = (a[i - 1, j] + a[i, j - 1] -
                       (a[i - 1, j - 1] if S[i - 1] != T[j - 1] else 0)) % MOD


def main():
    N, M = map(int, input().split())
    S = np.fromstring(input(), dtype=np.uint32, sep=' ')
    T = np.fromstring(input(), dtype=np.uint32, sep=' ')
    a = np.ones((N + 1, M + 1), dtype=np.uint32)
    calc(a, S, T)
    print(a[N, M])


if __name__ == "__main__":
    main()