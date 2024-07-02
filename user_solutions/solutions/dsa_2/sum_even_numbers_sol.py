def sum_even_numbers(list):
    sum = 0
    for num in list:
        if num % 2 == 0:
            sum += num
    return sum