'''
goal - find p and q for a ~40 bit rsa key
'''

from random import randint
from math import ceil, sqrt


def fermat_is_prime(n, k=100) -> bool:
    ''' return true if likely prime '''
    for i in range(k):
        a = randint(2, n-2)
        if pow(a, n-1, n) != 1:
            return False
    return True

def full_is_prime(n) -> bool:
    ''' return true if actually prime '''
    for i in range(2, ceil(sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

if __name__ == '__main__':
    found = 0
    for i in range(2**20+1, 2**30, 2):
        if fermat_is_prime(i):
            if full_is_prime(i):
                print(i)
                found += 1
                if found >= 2:
                    break
