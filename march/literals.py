'''
goal - figure out the optimal way to build numbers in piet
       use color block size of 1
'''


instructions = {'p': 'push',
                'd': 'duplicate',
                'a': 'add',
                'm': 'multiply',
                's': 'subtract'}

ans = {1: 'p'}
ans_attr = {1: 'base'}


def _prime_factors(n):
    i = 2
    factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    factors.sort()
    f = {}
    x = factors[0]
    xn = 0
    for i in factors:
        if i == x:
            xn += 1
        else:
            f[x] = xn
            x = i
            xn = 1
    f[x] = xn
    return f


'''
methods:
    - binary; get binary representation, construct powers of 2 and add them
    - factors; get prime factors, mult them
    - dec; try down by 1
'''


def best(n: int, a='') -> str:
    global ans
    if n < 0:
        raise Exception('Not implemented yet')
    if n == 0:
        return a
    if n == 1:
        return a+'p'  # simple base case
    if n in ans:
        return ans[n]
    mx = [methods[0](n, ''), methods[0].__name__]
    for method in methods[1:]:
        x = method(n, a)
        if len(x) < len(mx[0]):
            mx = x, method.__name__
    ans[n] = mx[0]
    ans_attr[n] = mx[1]
    return ans[n]


def bin1(n: int, a: str) -> str:
    '''either add 1 or shift'''
    assert n >= 2

    n1 = n
    if n % 2 == 1:
        n1 -= 1
        a = 'pa' + a
    else:
        n1 >>= 1
        a = 'da' + a
    return best(n1) + a


def bin2(n: int, a: str) -> str:
    '''convert to bin, sum 1's'''
    assert n >= 2
    bin_str = bin(n)[:1:-1]  # cut off 0b and reverse
    extra_add = 0
    a = 'p'
    for i in range(len(bin_str[:-1])):
        if bin_str[i] == '1':
            a += 'd'  # save
            a += 'da'  # shift
            extra_add += 1
        else:
            a += 'da'  # shift
    a += 'a' * extra_add
    return a


def fact(n: int, a: str) -> str:
    '''get prime factorization, product them'''
    assert n >= 2
    p = _prime_factors(n)
    if len(p) == 1 and sum(p.values()) == 1:
        # the number is prime, use something else
        return '-' * 100
    for i in p:
        # make the number
        a += best(i)
        # duplicate it
        a += 'd' * (p[i]-1)
    # product
    a += 'm' * (sum(p.values())-1)
    return a


def dec(n: int, a: str) -> str:
    assert n >= 2
    a += 'pa'
    return a + best(n-1)


methods = [bin2, bin1, fact]


def test():
    for i in range(20):
        print(best(i))
    print(ans)
    print(ans_attr)


def test2():
    for i in range(1000):
        best(i)

    vals = list(ans_attr.values())
    for i in set(vals):
        print(i, vals.count(i))


def test3():
    print(len(best(2**40)))
    print(ans[2**40])
    print(ans_attr[2**40])


def test4():
    for i in range(2**40):
        best(i)
    print(len(best(2**40)))


if __name__ == '__main__':
    test4()
