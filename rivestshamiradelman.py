from Crypto.Util import number
import math
from random import randint

strength_length = 128
# Get the two primes that make up the composite modulus
# They should not be too close, otherwise N can be factored by fermat's method
# i.e. using a^2 - b^2 = (a-b)(a+b)
# Does not apply here since they are independently chosen
sl1 = int(math.floor(strength_length/2))
# Ceils and Floors just in case anyone is crazy enough to use an odd length number
sl2 = int(math.ceil(strength_length/2))
prime1 = number.getPrime(sl1)
prime2 = number.getPrime(sl2)

print("First prime", prime1, len(str(prime1)))
print("Second prime", prime2, len(str(prime2)))

# The modulus is public
modulus = prime1 * prime2
print("The modulus", modulus, len(str(modulus)))

# Vary nice, now to calculate the Carmichael function for N, so that we can find e and d later
# The function calculates the value of m for N such that all a from 1 to N-1, a^(m) = 1 mod N
# It's a little different from the Euler's totient function but, they are the same for primes
# This is made much simpler considering that N is a product of two primes
gcd_primes_effect = math.gcd(prime1-1, prime2-1)
lcm_primes_effect = (prime1-1)*(prime2-1)/gcd_primes_effect
lcm_primes_effect = int(lcm_primes_effect)
carmichael_result = lcm_primes_effect
print("The totient function of the modulus", carmichael_result)

# Choosing the RSA exponents
# e is standard, and it's kept small for fast encryption
# Good practice suggests that e is 65537, that is 1<<16 + 1, this is secure
# Why is this more secure than any other random number?
# d is the modular inverse wrt module carmichael(N)
encrypt_exp =  65537

def modular_invert_euclidean(a, n):
    """
    Find the inverse of a wrt modulo n.
    Uses the extended euclidean algorithm.
    Makes use of the fact that the equation is in the form of Bezout's identity
    ax mod n = 1
    """
    x = 0
    new_x = 1
    r = n
    new_r = a

    while new_r:
        quotient = r // new_r
        (x, new_x) = (new_x, x - quotient*new_x)
        (r, new_r) = (new_r, r - quotient*new_r)

    if r > 1:
        return None
    if x < 0:
        return x + n

    return x

decrypt_exp = modular_invert_euclidean(encrypt_exp, carmichael_result)
if not decrypt_exp:
    print("Could not find a decryption exponent, quitting")
    exit()
# Verify that the pair generated is valid
assert (encrypt_exp*decrypt_exp % carmichael_result) == 1

print("Encryption exp:", encrypt_exp, "Decryption exp:", decrypt_exp)

# The future of the key - generation results and side-results
# prime1 and prime2 - dangerous, delete
# modulus - required, public knowledge
# encryption exponent - required, public knowledge
# carmichael result - dangerours, delete
# decryption exponent - required, private knowledge

del prime1
del prime2
del carmichael_result

N = modulus
e = encrypt_exp
d = decrypt_exp

# Sharing keys and receiving messages
# e and N made public

# Communication, Bob wants to send a number securely to Alice
# What Bob has secret - the secret message, the public key, the modulus
# This is a joke, this is not secure, there are chosen cipher-text attacks against it
# To use RSA to securely send secrets such as AES keys, use OAEP, since PKCS is broken
# Another limitation on the secret message is that it has to smaller than the modulus
secret = randint(1, 42069666)
m = secret
print("The plain-text message:", secret)
# Surpise! Surpise! Python has an inbuilt fast modular exponent calculator
encrypted_secret = pow(m, e, N) 
c = encrypted_secret
print("The cipher-text:", encrypted_secret)

# Bob sends c to Alice
print("Alice received the cipher text")
decrypted_secret = pow(c, d, N)
alice_m = decrypted_secret
print("The message Alice decrypted:", decrypted_secret)
print(alice_m == m)
