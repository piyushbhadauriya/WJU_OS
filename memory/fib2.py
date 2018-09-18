def fib(n):
    i = 2
    x = 1
    y = 1
    while (i < n):
        tmp = x+y
        x=y
        y=tmp
        i= i+1
    return y

print(fib(10))