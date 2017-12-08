#1. implement MGF1, use sha1
# This function takes an input string of arbitrary length and outputs a string of
# (almost) arbitrary length.
#2.  implement I2OSP
from H0 import *
import math

def mgf1(mgfSeed, maskLen):
    T = bytearray()
    hLen = 20
    for counter in range (math.ceil(maskLen / hLen)):
        C = i20sp(counter, 4)
        T = T + hashStuff(hexaToByte(mgfSeed) + C)
    return byteToHexa(T[:maskLen])

def i20sp(x, xLen):
    values = []
    for i in range(xLen):
        rest = x % 256
        values.append(rest)
        x //= 256
    return bytes(values[::-1])

def oaep_encode(m, seed, l=b''):
    hLen = 20
    mLen = len(m) // 2
    lHash = hashlib.sha1(l).digest()
    #k = 128
    k = 128
    l1 = k - mLen - 2*hLen - 2
    l2 = k - hLen -1
    PS = i20sp(0, l1)
    DB = lHash + PS + i20sp(1, 1) + hexaToByte(m)
    dbMask = hexaToByte(mgf1(seed, l2))
    #fylla ut DB och maskedDB
    maskedDB = bytes(a^b for a,b in zip(DB, dbMask))
    seedMask = hexaToByte(mgf1(byteToHexa(maskedDB), hLen))
    maskedSeed = bytes(a^b for a,b in zip(hexaToByte(seed), seedMask))
    EM = i20sp(0, 1) + maskedSeed + maskedDB
    return byteToHexa(EM)

def oaep_decode(EM):
    hLen = 20
    lHash = hashlib.sha1().digest()
    k_hLen_1 = 128 - hLen -1
    EM = hexaToByte(EM)
    maskedSeed = EM[1:hLen+1]
    maskedDB = EM[hLen+1:]
    seedMask = hexaToByte(mgf1(byteToHexa(maskedDB), hLen))
    seed = bytes(a^b for a,b in zip(maskedSeed, seedMask))
    dbMask = hexaToByte(mgf1(byteToHexa(seed), k_hLen_1))
    DB = bytes(a^b for a,b in zip(maskedDB, dbMask))[hLen:]
    M_index = DB.index(1) + 1
    M = DB[M_index:]
    return byteToHexa(M)

# mgfSeed = "0123456789abcdef"
# maskLen = 30
# mgfSeed = "9b4bdfb2c796f1c16d0c0772a5848b67457e87891dbc8214"
# maskLen = 21
# m = "c107782954829b34dc531c14b40e9ea482578f988b719497aa0687"
# seed = "1e652ec152d0bfcd65190ffc604c0933d0423381"
mgfSeed = "54bacfd9ce645dad640fbd5b83123c2e3fa90f3b8fcb"
maskLen = 22
m = "ebabeb71c16a063cffa28be88bf8216d909c951c86de8c86e01de9"
seed = "62d355c9abd4cd50744b0a864ae809214fcea72e"
print("mask: " + mgf1(mgfSeed, maskLen))
EM = oaep_encode(m, seed)
print("EM: " + EM)
em = "0043759f100e1b0ffbaed6b5e234f085cfd20cb94962f786195f85f8d337481f2abb06da0f3f9b1a5e413d31e347a179461d13c47b4f6893c02220932443e5764a02e5e0233d76bbdbc5c2e65c3dc014dd42a6532a2b5dcf4327381adfb17506a65397e78b611b2080a5d90a4818eea05072f5cc639ae55f1c7462da3621dcd0"
DM = oaep_decode(em)
print("DM: " + DM)
