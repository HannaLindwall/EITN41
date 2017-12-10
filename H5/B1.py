#PEM is Base64 of DER
from Crypto.PublicKey import RSA
import sys
from H0 import *
sys.setrecursionlimit(1000000)
import base64
from Crypto.Hash import SHA
from Crypto import Random
from Crypto.Cipher import PKCS1_v1_5

def restore_key(em):
    #f = open('key.pem','r')
    #f = open('test_pem.pem','r')
    f = open('quiz_key.pem','r')
    key = RSA.importKey(f.read())
    d = key.d
    n = key.n
    u = key.u

    e = key.e
    p = key.p
    q = key.q
    new_n = p * q
    phi = (p-1) * (q-1)
    new_d = mulinv(e, phi)
    new_key = RSA.construct((new_n, e, new_d))
    m = decrypt_message(new_key, em)
    return new_key.exportKey(), m

def decrypt_message(key, em):
    unbasefied_em = base64.b64decode(em)
    dsize = SHA.digest_size
    sentinel = Random.new().read(15+dsize)
    cipher_std = PKCS1_v1_5.new(key)
    m = cipher_std.decrypt(unbasefied_em, sentinel)
    return m

def mulinv(e, phi):
    g, x, _ = egcd(e, phi)
    if g == 1:
        return x % phi

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = egcd(b % a, a)
        return (g, y - (b // a) * x, x)

# m = "Qe7+h9OPQ7PN9CmF0ZOmD32fwpJotrUL67zxdRvhBn2U3fDtoz4iUGRXNOxwUXdJ2Cmz7zjS0DE8ST5dozBysByz/u1H//iAN+QeGlFVaS1Ee5a/TZilrTCbGPWxfNY4vRXHP6CB82QxhMjQ7/x90/+JLrhdAO99lvmdNetGZjY="
if __name__ == '__main__':
    # m = "T9FAfFVcVCdPH45kv3OU/Kot9NOyQ2t5tWI1GW6nJ4Ul435T68wq1f1vm3KhDcKONzdN3krJ/VwlIzdssIcqmVizw5mnMupmd1gNmf7EKLZWjT4LaMQhDMijrfhxCdbiQKjKqYnUehlOCeDS0JXOJpiYcCtbmTVYHBmxBuOZ1l8="
    m = "t2JtdjaM71d67nvC9CZZ5kpumAmY9LrEh8//OdUKX+xvv+UG+9tvM/9P/Aen/tW21FFfNUWPKm+EkuHjecvMa5KqZqVoXKNqVz4Ke4p1fL1eVdUpJ8Rnj5XoI9Bg2RVK0ZgTqsllUzKzaTfrkvQcya+qUTLCruT+JeRgdrsdTKE="
    key, m = restore_key(m)
    print("key: ", key.decode("utf-8"))
    print("message: ", m.decode("utf-8"))
