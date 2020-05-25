from random import randint
from Crypto.PublicKey import RSA
from Crypto.Random import random
import zmq


PORT = 8042
LEN_NUMS = 4096
ORDER = 'little'


def ot12(public_key, choice, socket):
    """
    The one out of two oblivious transfer protocol but for the client
    For more details look at the oblivious transfer file
    """
    e = public_key.e
    n = public_key.n
    blind = random.getrandbits(512)
    r0 = socket.recv()
    r1 = socket.recv()
    r0 = int.from_bytes(r0, byteorder=ORDER)
    r1 = int.from_bytes(r1, byteorder=ORDER)
    rands = [r0, r1]
    secret_i = (rands[choice] + pow(blind, e, n)) % n
    secret_i = secret_i.to_bytes(LEN_NUMS, byteorder=ORDER)
    socket.send(secret_i)
    hm0 = socket.recv()
    hm1 = socket.recv()
    hm0 = int.from_bytes(hm0, byteorder=ORDER)
    hm1 = int.from_bytes(hm1, byteorder=ORDER)
    messages = [hm0, hm1]
    chosen = messages[choice]
    required = chosen - blind
    return required


# Setting up a two way connection
context = zmq.Context()
socket = context.socket(zmq.PAIR)
socket.connect(f"tcp://localhost:{PORT}")

# The client gets access the public key
with open('rsapublic.pem', 'rb') as red:
    pubkey = RSA.import_key(red.read())

# An example to show that ot12 works in its intended role
"""
choice = 0
result = ot12(pubkey, choice, socket)
print(result)
"""

# The actual processing, goal - read message i for some i belonging to n
# Set up the common constants
n = 100
length = 64

# Store all the key's until the correct turn
k_store = []

# Pick i, the index
i = randint(1, n)
print("Chose the index", i)

# Run the main loop
for j in range(1, n+1):
    if j != i:
        k_tmp = ot12(pubkey, 1, socket)
    else:
        m_tmp = ot12(pubkey, 0, socket)

    if j < i:
        k_store.append(k_tmp)
# print(k_store)
# print(m_tmp)

# Calculate the message
k_xor = 0
for key in k_store:
    k_xor ^= key
message = k_xor ^ m_tmp
print("Got the message without revealing the index")
print(message)
