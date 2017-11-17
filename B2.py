# Write a program that simulates the time needed to generate MicroMint coins.
# Model the process as a balls-and-bins problem.
# Your program should take three parameters;
# u - is the number of bits used for identifying the bin
# k - is the number of collisions (balls in the same bin) needed to make
# a coin, so that fewer than k balls in a bin make no coins, and k or more balls
# in a bin make precisely one coin. Bins start empty.
# c - number of coins
import hashlib
from H0 import *
from random import * #för att inte behöva skriva random framför allt
from math import *
from numpy import *

def createCoins(u, k, c):
    nbr_coins = 0
    bins = [0 for x in range(2**u)]
    tries = 0
    while (nbr_coins < c):
        rand_value = randrange(0, 2**(2*u))
        hash_array = hashStuff(intToByte(rand_value))
        index = round(byteToInt(hash_array) % 2**u)
        bins[index] += 1
        if (bins[index]==k):
            nbr_coins += 1
        tries += 1
    return tries

def get_them_stats(u, k, c, width):
    x = []
    w = width + 1
    lamnda = 3.66
    n = 0
    x.append(createCoins(u, k, c))
    mean_x = mean(x)
    n += 1
    s = std(x)
    while (w >= width):
        x.append(createCoins(u, k, c))
        mean_x = mean(x)
        n += 1
        s = std(x)
        w = (mean_x + lamnda * s / sqrt(n)) - (mean_x - lamnda * s / sqrt(n))
    print("Average x: ", mean_x, "for ", c, " # of coins\n")


# get_them_stats(16, 2, 1, 22) #324
# get_them_stats(16, 2, 100, 24) #3684
# get_them_stats(16, 2, 10000, 22) #45261
# get_them_stats(20, 7, 1, 79671) #482437
# get_them_stats(20, 7, 100, 15616) #1080572
get_them_stats(20, 3, 10000, 660) #2418038
