from functools import lru_cache


@lru_cache(maxsize=None)
def fibonacci(n):
    """Return the nth Fibonacci number using caching."""
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    else:
        seq = fibonacci(n - 1)
        seq.append(seq[-1] + seq[-2])
        return seq


def fibonacci_sequence(n):
    """Generate Fibonacci sequence for first n digits."""
    return fibonacci(n)


N = 10
for num in fibonacci_sequence(N):
    print(num)
