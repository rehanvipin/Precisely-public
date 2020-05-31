from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Random.random import getrandbits
from Crypto.Cipher import ChaCha20
from Crypto.Util.Padding import unpad
import zmq
import pickle

# some constants, length of label, pad length
LABEL_LEN = 32
PAD_LEN = 32
PORT = 8042
LEN_NUMS = 4096
ORDER = 'little'


# Oblivious transfer to get chosen value
def ot12(public_key, choice, socket):
    """
    The one out of two oblivious transfer protocol but for the client
    For more details look at the oblivious transfer file
    """
    e = public_key.e
    n = public_key.n
    blind = getrandbits(512)
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


# Utility function to decrypt values
# Only one of the values passed to this function will not return None
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


def evaluate(socket, einput, publickey):
    """
    Gets the permuted truth table from the server
    comms through the socket,
    evaluates them by trying all the combinations
    Sends evaluated result back
    """

    # Get the permuted encrypted truth table
    # It's pickled, unpickle first
    container = socket.recv()
    truth_table = pickle.loads(container)
    # Get the input label from the server
    server_in = socket.recv()
    # Get own input from the server
    client_in = ot12(publickey, einput, socket)
    client_in = client_in.to_bytes(LABEL_LEN, byteorder='little')

    # decrypt the correct value
    correct = b"FAILED"
    for garbled in truth_table:
        cltr = decrypt(server_in, client_in, garbled)
        if cltr:
            correct = cltr
    socket.send(correct)
    return correct.decode()


# Get the rsa key(public) from disk
with open('rsapublic.pem', 'rb') as red:
    pubkey = RSA.import_key(red.read())

# The client is the evaluator
# It receives the permuted truth table
# And decrypts all of them and choosing the correct one
context = zmq.Context()
socket = context.socket(zmq.PAIR)
socket.connect(f"tcp://localhost:{PORT}")

# The input from the evaluator
client_input = getrandbits(1)
print("The evaluator's input", client_input)
result = evaluate(socket, client_input, pubkey)
print("Got the result", result)
