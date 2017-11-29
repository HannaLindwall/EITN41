import random
import math


def threshold_scheme(k,n, my_pol,revealed, shared, me):
    f0 = 0
    revealed[me-1] = calculate_my_value(pol, shared, me)
    for i in range(0, len(revealed)):
        if(revealed[i] != 0):
            divs = 1
            for j in range(0, len(revealed)):
                if(j != i and revealed[j]!=0):
                    divs *= (j+1) / ((j+1) - (i+1))
            f0 += revealed[i] * divs
    print(round(f0))


def calculate_my_value(my_pol, shared, me):
    my_value = 0
    for i in range(0, len(my_pol)):
        my_value += my_pol[i] * me**(i+1)
    return my_value + sum(shared)

# k = 5
# n = 8
# pol = [13, 8, 11, 1, 5]
# revealed = [0, 2782, 0, 30822, 70960, 0, 256422, 0]
# shared = [75, 75, 54, 52, 77, 54, 43]
# me = 1
# k = 5
# n = 6
# pol = [20, 18, 13, 19, 15]
# revealed = [0, 1908, 7677, 0, 50751, 101700]
# shared = [34, 48, 45, 39, 24]
# me = 1
# k = 3
# n = 6
# pol = [9, 19, 5]
# revealed = [0, 0, 0, 1385, 2028, 0]
# shared = [37, 18, 40, 44, 28]
# me = 1
k = 4
n = 6
pol = [20, 20, 11, 6]
revealed = [0, 0, 2199, 4389, 0, 12585]
shared = [63, 49, 49, 54, 43]
me = 1
# k =
# n =
# pol = []
# revealed = []
# shared = []
# me =
threshold_scheme(k,n,pol, revealed, shared, me)
