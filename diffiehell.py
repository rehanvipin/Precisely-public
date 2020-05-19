from typing import List
from Crypto.Util import number
from random import randint
nice_prime = number.getPrime(16)
#print(nice_prime)

def find_factors(numba: int) -> List[int]:
    factor = 2
    factors = set()
    try:
        while factor <= numba:
            while numba%factor == 0:
                factors.add(factor)
                numba = int(numba/factor)
            factor += 1
    # Print progress when printing
    except KeyboardInterrupt as k:
        print(factor, factors)
    return list(factors)

# The order of a prime is always prime - 1
order_prime = nice_prime - 1
factors = find_factors(order_prime)
powers_to_test = [int(order_prime/factor) for factor in factors]
print(factors)
#print(powers_to_test)

# Now test the powers for each value from 2 until the prime, until we find a primitive root
def check(test: int, powers_to_test: List[int], prime: int):
    for power in powers_to_test:
        if (test**power)%prime == 1:
            return False
    return True
found = False
test = 2
while not found and test < nice_prime:
    found = check(test, powers_to_test, nice_prime)
    test += 1
prim_root = test

#print(prim_root)

# There, we got p and g
p = nice_prime
g = prim_root

# Alice's turn
a = randint(2, p-1)
ga = (g**a) % p
print(f"Alice's secret : {a}, public : {ga}")


# Bob's turn
b = randint(2, p-1)
gb = (g**b) % p
print(f"Bob's secret : {b}, public : {gb}")

print("Their shared secret key:")
print(f"By Alice : {(gb**a)%p}")
print(f"By Bob : {(ga**b)%p}")

print(f"Public knowledge - g:{g}, p:{p}, g^a:{ga}, g^b:{gb}")
