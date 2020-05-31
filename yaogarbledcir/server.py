from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Random.random import getrandbits
from Crypto.Random.random import shuffle
from Crypto.Cipher import ChaCha20
from Crypto.Util.Padding import pad
import zmq
import pickle


# some constants, length of label, pad length
LABEL_LEN = 32
PAD_LEN = 32
PORT = 8042
LEN_NUMS = 4096
ORDER = 'little'


# An auxillary function to return the ciphertext
def encryptstate(keyl, keyr, bit):
    lv1 = ChaCha20.new(key=keyr)
    ct1 = lv1.encrypt(keyl)
    nc1 = lv1.nonce
    lv2 = ChaCha20.new(key=ct1)
    pt2 = bytes(str(bit), encoding="utf8")
    pt2 = pad(pt2, PAD_LEN)
    ct2 = lv2.encrypt(pt2)
    nc2 = lv2.nonce
    return {"ct": ct2, "nc1": nc1, "nc2": nc2}


def ot12(private_key, choices, socket):
    """
    Execute one round of one out of two oblivious transfer
    For details look at that file
    """
    random0 = getrandbits(512)
    random1 = getrandbits(512)
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


def send_garbled(TRUTH_TABLE, socket, ginput, privatekey):
    """
    Sends a permuted truth table to the evaluator
    comms happen through the socket,
    ginput is the server's input to the gate.
    Receives the result from the evaluator.
    """
    GLabels = [get_random_bytes(LABEL_LEN) for _ in range(2)]
    ELabels = [get_random_bytes(LABEL_LEN) for _ in range(2)]
    ciphers = []
    # Collect all the ciphers using the labels
    for ip, op in TRUTH_TABLE.items():
        cipher = encryptstate(GLabels[ip[0]], ELabels[ip[1]], op)
        ciphers.append(cipher)
    shuffle(ciphers)
    # Send all the ciphertexts
    ciphertext = pickle.dumps(ciphers)
    socket.send(ciphertext)
    # Send the key corresponding to the garbler's input
    gin_send = GLabels[ginput]
    socket.send(gin_send)
    # Obliviously send the label the evaluator wants
    t_ELabels = [int.from_bytes(x, byteorder='little') for x in ELabels]
    ot12(privatekey, t_ELabels, socket)
    # Get the result from the evaluator
    result = socket.recv()
    return result.decode()


# Get the rsa key(private) from the file
with open('rsaprivate.pem', 'rb') as red:
    privkey = RSA.import_key(red.read())

# The server is the garbler here
# Making the truth table and sending the ciphertexts
# Communications happen over a network
# Make sockets for connections
context = zmq.Context()
socket = context.socket(zmq.PAIR)
socket.bind(f"tcp://*:{PORT}")

# Define the truth table of the two bit
# logic gate, change this to change operation
TRUTH_TABLE = {(0, 0): 0,
               (0, 1): 0,
               (1, 0): 0,
               (1, 1): 1}
choice = input("Want to make your own gate (default:AND) ? (y/n): ")
if choice.lower() == 'y':
    print("Enter the outputs for:")
    x00 = int(input("Enter output for 0,0: "))
    x01 = int(input("Enter output for 0,1: "))
    x10 = int(input("Enter output for 1,0: "))
    x11 = int(input("Enter output for 1,1: "))
    TRUTH_TABLE[(0, 0)] = x00
    TRUTH_TABLE[(0, 1)] = x01
    TRUTH_TABLE[(1, 0)] = x10
    TRUTH_TABLE[(1, 1)] = x11

# The input from the garbler
server_input = getrandbits(1)
print("The garbler's input", server_input)
result = send_garbled(TRUTH_TABLE, socket, server_input, privkey)
print("Got the result", result)
