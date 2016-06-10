# Project Euler Problem 2 - Even Fibonacci Numbers
# =====================================================

def fibonacci():
    a = 1
    b = 0
    sum = 0
    i = 0

    while b < 4000000:
        temp = a
        a = b
        b = temp + b
        if b % 2 == 0:
            sum += b

    print "The sum of all even Fibonacci numbers below 4,000,000 is: %d.\n" % sum


fibonacci()


# For this solution I have use an iterative dynamic programming approach for efficiency
