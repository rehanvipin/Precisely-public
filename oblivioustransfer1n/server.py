from Crypto.PublicKey import RSA
from Crypto.Random import random
import zmq
from tqdm import tqdm
# from random import randint

PORT = 8042
LEN_NUMS = 4096
ORDER = 'little'


def ot12(private_key, choices, socket):
    """
    Execute one round of one out of two oblivious transfer
    For details look at that file
    """
    random0 = random.getrandbits(512)
    random1 = random.getrandbits(512)
    d = private_key.d
    n = private_key.n
    r0 = random0.to_bytes(LEN_NUMS, byteorder=ORDER)
    r1 = random1.to_bytes(LEN_NUMS, byteorder=ORDER)
    socket.send(r0)
    socket.send(r1)
    secret_i = socket.recv()
    secret_i = int.from_bytes(secret_i, byteorder=ORDER)
    guess_0 = pow((secret_i - random0), d, n)
    guess_1 = pow((secret_i - random1), d, n)
    hm0 = (guess_0 + choices[0]) % n
    hm1 = (guess_1 + choices[1]) % n
    hm0 = hm0.to_bytes(LEN_NUMS, byteorder=ORDER)
    hm1 = hm1.to_bytes(LEN_NUMS, byteorder=ORDER)
    socket.send(hm0)
    socket.send(hm1)


# The server has access to the private keys of the communication
with open('rsaprivate.pem', 'rb') as red:
    private_key = RSA.import_key(red.read())

# Setting up a two way communication
context = zmq.Context()
socket = context.socket(zmq.PAIR)
socket.bind(f"tcp://*:{PORT}")

# An example to show that ot12 works on its own
"""
messages = [randint(0, 100), randint(0, 100)]
ot12(private_key, messages, socket)
"""

# The actual full one out of n OT, from the server
# Get all the messages, but define n before that
n = 100
length = 64
messages = [random.getrandbits(length) for _ in range(n)]
# print(messages)
print(f"Running the oblivious transfer protocol for {n} messages")

# choose the key to hide the messages
k_xor = 0  # the inital k0 is 0


# The actual working loop
for j in tqdm(range(1, n+1), position=0):
    k_j = random.getrandbits(length)
    message_choice = k_xor ^ messages[j-1]
    key_choice = k_j
    ot12(private_key, [message_choice, key_choice], socket)
    k_xor ^= k_j
    # print("Finished round", j)

choice = int(input("Enter the index to verify the result: "))
print("The correct anwser is", messages[choice-1])
