# Project Euler Problem 1 - Multiples of 3 and 5
# =============================================================

i = 0
sum = 0

while i < 1000:
    if i % 3 == 0 or i % 5 == 0:
        sum += i
    i += 1

print "Sum of multiples of 3 and 5 for numbers below 1000 is:\n" \
      "%d\n" % sum
