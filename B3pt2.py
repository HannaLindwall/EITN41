import hashlib
from H0 import *
from random import * #för att inte behöva skriva random framför allt
from math import *
from numpy import *
import fileinput



def find_depth(leaves):
    #assume valid index and depth
    index = int(leaves[0])
    depth = int(leaves[1])
    del leaves[0]
    del leaves[0]
    actual_depth = int(ceil(log2(len(leaves))))
    print(actual_depth)
    if(len(leaves) > 1):
        tree = get_total_tree(leaves, actual_depth)
        root = tree[actual_depth][0]
        i = actual_depth
        j = 0
        path = ""
        temp = ""
        while(i > 0):
            if(index % 2 == 0):
                temp = "R" + tree[j][index + 1]
            else :
                temp = "L" + tree[j][index - 1]
            if(i == depth):
                node_j = temp
            path = path + temp + "\n"
            index = int(index / 2)
            j += 1
            i -= 1
        return path, node_j, root
    else:
        if(len(leaves)==1):
            return (leaves[0], leaves[0], leaves[0])
        else:
            return "no nodes", "no nodes", "no nodes"

def get_total_tree(leaves, depth):
    tree = [[] for x in range(depth+1)]
    tree[0] = leaves
    for i in range (1, (depth+1)):
        level = []
        j = 0

        if(len(leaves) % 2 != 0 and i != depth):
            leaves.append(leaves[-1])
            print(leaves[-1])
        print(len(leaves))
        while(j < len(leaves)):
            temp = leaves[j] + leaves[j+1]
            temp = byteToHexa(hashStuff(hexaToByte(temp)))
            level.append(temp)
            j = j + 2

        tree[i] = level
        print(level)
        leaves = level
    return tree


merkle_leaves = []
for line in fileinput.input():
    merkle_leaves.append(line.strip())

path_i, node, root = find_depth(merkle_leaves)

print(path_i)
print(node)
print(root)
