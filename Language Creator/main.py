def f(n: int, orig=None) -> int:
    if orig == None:
        orig = n

    x = orig * (n == 1)

    for i in range(1, n):
        x += f(i, orig) 

    return x

print(f(8))