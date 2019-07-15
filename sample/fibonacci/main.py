from numba import jit, njit


@njit('i8(i8)')
def fib(n):
    if n < 2:
        return n
    else:
        return fib(n - 2) + fib(n - 1)


def main():
    print(fib(30))


if __name__ == "__main__":
    main()