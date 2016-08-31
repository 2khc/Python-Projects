import math
import random


def largest_prime_factor(n):
    # number = n
    i = 3
    largest = 0
    while i < n / 2:
        if n % 2 == 0:
            return largest_prime_factor(n / 2)
        elif n % i == 0 and check_prime(i):
            largest = i
        i += 1
    return largest


def check_prime(n):
    q = 1
    s = 0

    for i in range(0, n):
        power = pow(2, i)

        if (n - 1) % power == 0:
            q = (n - 1) / power
            if q % 2 == 1:
                s = i
                break

    a = random.randrange(1, n, 1)
    if pow(a, q) == 1:
        return True

    for i in range(0, s):
        if pow(a, pow(2, i) * q) == -1:
            return True

    return False

def aks_prime(n):




print largest_prime_factor(13195)
