def multiples_of_3_or_5(n):
    sum = 0
    if n < 0:
        return 0
    else:
        for i in range(n):
            if i % 3 == 0 or i % 5 == 0:
                sum += i
    return sum
