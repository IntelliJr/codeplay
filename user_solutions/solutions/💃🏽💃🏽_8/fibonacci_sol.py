def fibonacci(n):
    if n <= 0 or not isinstance(n, int):
        return -1
    elif n == 1:
        return 0
    elif n == 2:
        return 1
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)