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
    fake_v, fake_k, matches = alice_v^1, 0, 0
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
    k, zersies, onesies = 0, 0, 0
    while( k < 2**16 ):
        zero_commit = create_commit(0, k, X)
        one_commit = create_commit(1, k, X)

        if(zero_commit == alice_commit):
            zersies += 1
        if(one_commit == alice_commit):
            onesies += 1
        k += 1
    print(zersies, " ", onesies)
    nom = zersies if alice_v==0 else onesies

    print(nom/(zersies+onesies), " ", nom)
    return nom / (zersies + onesies)

max_X = 25
prob_binding = []
prob_concealing = []
dnom = 10
for X in range(max_X):
    alice_v = random.randint(0,1)
    k = get_random_k()
    alice_commit = create_commit(alice_v, k, X)

    print(X)

    binding = [break_binding(alice_commit, k, alice_v, X) for i in range(dnom)]
   concealing = [break_concealing(alice_commit, alice_v, X) for i in range(dnom)]

    prob_binding.append(sum(binding) / dnom)
   prob_concealing.append(sum(concealing) / dnom)

plt.plot(range(max_X), prob_binding, label='binding')
plt.plot(range(max_X), prob_concealing, label='breaking')
plt.xlabel("X")
plt.show()
