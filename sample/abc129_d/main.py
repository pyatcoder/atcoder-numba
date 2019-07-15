import numpy as np
import sys
from numba import njit


@njit('void(i4[:,:])')
def calc(a):
    # 横方向
    for j in range(a.shape[0]):
        prev = 0
        start = 0
        for i in range(a.shape[1]):
            if a[j, i] > 0:
                if prev == 0:
                    start = i
                    prev = 1
            else:
                if prev == 1:
                    num = i - start
                    for k in range(start, i):
                        a[j, k] = num
                    prev = 0
    # 縦方向
    for i in range(a.shape[1]):
        prev = 0
        start = 0
        for j in range(a.shape[0]):
            if a[j, i] > 0:
                if prev == 0:
                    start = j
                    prev = 1
            else:
                if prev == 1:
                    num = j - start - 1
                    for k in range(start, j):
                        a[k, i] += num
                    prev = 0


def main():
    cin = sys.stdin.buffer
    H, W = map(int, cin.readline().split())
    a = np.empty((H + 1, W + 1), dtype='i4')
    a[:H, :] = (np.frombuffer(cin.read(H * (W + 1)), dtype='B') == ord('.')).reshape((H, W + 1))
    a[H] = np.zeros(W+1, dtype='i4')

    calc(a)
    print(a.max())


if __name__ == "__main__":
    main()
