from Crypto.Random import get_random_bytes
from Crypto.Random.random import getrandbits
from Crypto.Cipher import ChaCha20
from Crypto.Util.Padding import pad, unpad

import random


LABEL_LEN = 32
PAD_LEN = 32
# Garbled circuits, in a single file
# Ginny and Evan want to compute the and of both their hidden values
# Ginny is the garbler and Evan is the evaluator.

# Ginny's calculations
ginny_input = getrandbits(1)
# Now to pick labels
GLabels = [get_random_bytes(LABEL_LEN) for _ in range(2)]
ELabels = [get_random_bytes(LABEL_LEN) for _ in range(2)]
# print(ginny_input)
# print(GLabels)
# print(ELabels)

# The and function's truth table
tt_and = {(0, 0): 0, (0, 1): 0, (1, 0): 0, (1, 1): 1}


# A function to return the ciphertext
def create_table(keyl, keyr, text):
    lv1 = ChaCha20.new(key=keyr)
    ct1 = lv1.encrypt(keyl)
    nc1 = lv1.nonce
    lv2 = ChaCha20.new(key=ct1)
    pt2 = bytes(str(text), encoding="utf8")
    pt2 = pad(pt2, PAD_LEN)
    # print(pt2)
    ct2 = lv2.encrypt(pt2)
    nc2 = lv2.nonce
    return {"ct": ct2, "nc1": nc1, "nc2": nc2}


# Calculating the encrypted truth table
results = []
send = []
for key, val in tt_and.items():
    keyl = GLabels[key[0]]
    keyr = ELabels[key[1]]
    garbled = create_table(keyl, keyr, val)
    results.append((key, garbled))
    send.append(garbled)
# print(results)

# The cipher texts are ready
random.shuffle(send)

# Data to send to evan
send_pack = [send, GLabels[ginny_input]]


# Evan starts his computation
# Receive his label through oblivious transfer
# Replace with ot for a network program
evan_input = getrandbits(1)
received, glab = send_pack
elab = ELabels[evan_input]


# A function for evans to decrypt the table
# Only of the values passed to this function will not return None
def decrypt(keyl, keyr, ctns):
    lv1 = ChaCha20.new(key=keyr, nonce=ctns['nc1'])
    skey = lv1.encrypt(keyl)
    lv2 = ChaCha20.new(key=skey, nonce=ctns['nc2'])
    ptx = lv2.decrypt(ctns['ct'])
    try:
        clear = unpad(ptx, PAD_LEN)
    except ValueError:
        return None
    return clear


# Try decrypting all the values in the truth table, save the correct one
correct = b'0'
for garbled in received:
    # print(garbled)
    cltr = decrypt(glab, elab, garbled)
    if cltr:
        correct = cltr

# The calculation result is
final = correct.decode("utf8")
# This is sent to ginny
print("Performing the AND operation between")
print("Ginny", ginny_input)
print("Evan", evan_input)
print("Calculation result", final)
