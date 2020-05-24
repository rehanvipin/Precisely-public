from Crypto.PublicKey import RSA
from Crypto.Random import random

# The generate function generates both the public and private keys, it uses e = 1<<16 + 1
keys = RSA.generate(2048)
n = keys.n
p = keys.p
q = keys.q
e = keys.e
d = keys.d
u = keys.u # The remainder from the chinese remainder theorem
"""
print("n =",n)
print("p =",p)
print("q =",q)
assert n == p * q
print("e =",e)
print("d =",d)
assert pow(pow(42, e, n), d, n) == 42
"""

# Save the key to a file for later use
private_key = keys.export_key()
pubkey = keys.publickey().export_key()

# The structure : the private key has all the components described above, it can be used to encrypt and decrypt
# the public key is an object of the same type but has lesser information, it only has n and e, the two components
# Required to encrypt messages
"""
with open('rsa_private', 'wb') as wire:
    wire.write(private_key)
with open('rsa_pubkey', 'wb') as wire:
    wire.write(pubkey)
"""


# The 1 out of 2 oblivious transfer from Wikipedia

# Alice and what she has
message0 = 12345
message1 = 67890
random0 = random.getrandbits(512)
random1 = random.getrandbits(512)
print("Alice")
print("m0", message0)
print("m1", message1)
print("r0", random0)
print("r1", random1)
d = keys.d
n = keys.n
print("Initial communication done")

# Bob and what he has
rands = [random0, random1] # what he got from Alice
blinder = random.getrandbits(512)
index = random.getrandbits(1)
e = keys.e
n = keys.n # Both of these are sent by Alice
print("k", blinder)
print("b", index)
secret_choice = (rands[index] + pow(blinder, e, n)) % n
print("Comm sent to Alice")

# Alice decides to send messages securely
guess_blinder_0 = pow((secret_choice - random0), d, n)
guess_blinder_1 = pow((secret_choice - random1), d, n)
print("k'0", guess_blinder_0)
print("k'1", guess_blinder_1)
hidden_message_0 = guess_blinder_0 + message0
hidden_message_1 = guess_blinder_1 + message1
print("Messages sent to Bob")

# Bob picks the correct message and is happy
messages_recv = [hidden_message_0, hidden_message_1]
chosen_one = messages_recv[index]
free_read = chosen_one - blinder
print("Plaintext:", free_read)
