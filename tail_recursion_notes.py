"""A worked example with Fibonacci numbers, to demonstrate tail recursion in Python."""

# fibonacci, stack consuming
def fib(n):
    if n == 0:
        return 1

    return n * fib(n-1)


# tail recursive style
def fib2inner(n, accum):
    if n == 0:
        return accum

    return fib2inner(n - 1, n * accum) # would not consume stack if we had tail recursion

def fib2(n):
    return fib2inner(n, 1)


# continuation passing style
def fib3inner(n, continuation):
    if n == 0:
        return continuation(1)

    return fib3inner(n - 1, lambda x: continuation(x * n)) # still consumes stack

def fib3(n):
    return fib3inner(n, lambda x: x)


# tail recursive continuation passing
def fib4inner(n, accum, continuation):
    if n == 0:
        return continuation(accum)

    return fib4inner(n - 1, n * accum, continuation)

def fib4(n):
    return fib4inner(n, 1, lambda x: x)


# a trampoline gives us proper tail recursion
def trampoline(func):
    while callable(func):
        func = func()

    return func

# trampolined, tail recursive, passing a continuation
def fib5inner(n, accum, continuation):
    if n == 0:
        return lambda: continuation(accum)

    return lambda: fib5inner(n - 1, n * accum, continuation)

def fib5(n):
    return trampoline(fib5inner(n, 1, lambda x: x))
