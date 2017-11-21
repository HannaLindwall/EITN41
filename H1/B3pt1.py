import hashlib
from H0 import *
from random import * #för att inte behöva skriva random framför allt
from math import *
from numpy import *
import fileinput

def find_root(path):
    if(len(merkle_path)>1) :
        return rec_find_root(0, merkle_path[1])
    else :
        if(len(merkle_path)==1):
            return merkle_path[1]
        else :
            return "no nodes"


def rec_find_root(i, neighbor):
    neighbor1 = merkle_path[i]
    neighbor2 = neighbor

    if(neighbor1[0].isdigit()):

        if(neighbor2[0]=="R"):
            temp = neighbor1 + neighbor2[1:]
        else:
            temp = neighbor2[1:] + neighbor1
    else :
        if(neighbor1[0]=="R"):
            temp = neighbor2 + neighbor1[1:]
        else:
            temp = neighbor1[1:] + neighbor2

    temp = byteToHexa(hashStuff(hexaToByte(temp)))
    if(i == 0):
        i = 2
    else:
        i = i + 1

    if(i == len(merkle_path)):
        return temp
    else:
        return rec_find_root(i, temp)

merkle_path = []
for line in fileinput.input():
    merkle_path.append(line.strip())

root = find_root(merkle_path)
print(root)
