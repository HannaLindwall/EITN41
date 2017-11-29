import hashlib
import binascii
import random
import numpy as np
import matplotlib.pyplot as plt

def get_random_k():
    return random.randrange(0, 2**16)

def create_commit(v, k, X):
    random_byte = k.to_bytes(2, byteorder='big')
    cat_bytes = hashlib.sha1((v.to_bytes(1, byteorder='big') + random_byte)).digest()
    commit_int = int.from_bytes(cat_bytes, byteorder='big') % 2**X
    return commit_int

def break_binding(commit, k, alice_v, X):
    fake_v = alice_v^1
    fake_k = 0
    matches = 0
    while(fake_k < (2**16)):
        fake_commit = create_commit(fake_v, fake_k, X)
        #här skulle man kunna spara fake_k, så när Bob har revealat och ber
        # Alice att reveala så kan hon bara välja matchande för rätt gissning
        #antingen hennes första gissning eller hennes back-up gissning
        if(fake_commit == commit):
            return 1
        fake_k += 1
    return 0


def break_concealing(alice_commit, alice_v, X):
    k = 0
    #hur ska jag göra här för att inte dela med 0
    zersies = 0.00000001
    onesies = 0.00000001
    while( k < 2**16 ):
        if(create_commit(0, k, X) == alice_commit):
            zersies += 1
        if(create_commit(1, k, X) == alice_commit):
            onesies += 1
        k += 1
    nom = zersies if alice_v==0 else onesies
    dnom = zersies if nom==onesies else onesies
    return nom / dnom

max_X = 25
prob_binding = []
prob_concealing = []
dnom = 20
for X in range(max_X):
    alice_v = random.randint(0,1)
    k = get_random_k()
    alice_commit = create_commit(alice_v, k, X)

    print(X)

    binding, concealing = ([break_binding(alice_commit, k, alice_v, X) for i in range(dnom)],
                          [break_concealing(alice_commit, alice_v, X) for i in range(dnom)])


    prob_binding.append(sum(binding) / dnom)
    prob_concealing.append(sum(concealing) / dnom)

plt.plot(range(max_X), prob_binding, label='binding')
plt.plot(range(max_X), prob_concealing, label='binding')
plt.xlabel("X")
plt.show()
