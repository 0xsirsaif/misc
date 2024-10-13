# def foo(n):
#     x = []
#     for _ in range(n):
#         x.append(None)
#     return x
#
#
# foo(1_000_000)


def a(n):
    return [b(n), h(n)]


def b(n):
    return c(n)


def c(n):
    missing(n)
    return d(n)


def missing(n):
    return "a" * n


def d(n):
    return [e(n), f(n), "a" * (n // 2)]


def e(n):
    return "a" * n


def f(n):
    return g(n)


def g(n):
    return "a" * n * 2


def h(n):
    return i(n)


def i(n):
    return "a" * n


a(100000)
