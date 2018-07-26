import ed25519
import struct
import sha3
from binascii import hexlify
from binascii import unhexlify

def hex2int(hex):
    ## converts a hex string to integer
    return ed25519.decodeint(unhexlify(hex))

def int2hex(int):
    ## converts an integer to a little endian encoded hex string
    return hexlify(ed25519.encodeint(int))

def keccak_256(message):
    h = sha3.keccak_256()
    h.update(unhexlify(message))
    return h.hexdigest()

def sc_reduce32(input):
    ## convert hex string input to integer
    int = hex2int(input)
    ## reduce mod l
    modulo = int % (2**252 + 27742317777372353535851937790883648493)
    ## convert back to hex string for return value
    return int2hex(modulo)

def hash_to_scalar(key):
    hash = keccak_256(key)
    return sc_reduce32(hash)

def hash_to_ec(key):
    scalar = hash_to_scalar(key)
    ## convert to point on curve by multiplying the base point by the resulting scalar
    point = ed25519.scalarmultbase(scalar)
    ## multiply by 8 for security
    return ed25519.scalarmult(point, 8)

## multiply a public key (a point on the curve) by a private key (a scalar within the field p)
def generate_key_derivation(public, private):
    point = ed25519.scalarmult(ed25519.decodepoint(unhexlify(public)), hex2int(private))
    ##multiply by 8 for security
    res = ed25519.scalarmult(point, 8)
    ## return hex encoding of the resulting point
    return hexlify(ed25519.encodepoint(res))

def derivation_to_scalar(derivation, index):
    ## concatenate index to derivation
    data = derivation + index
    return hash_to_scalar(data)

## Alias for scalarmultbase
def publickey_to_privatekey(privateKey):
    point = ed25519.scalarmultbase(hex2int(privateKey))
    return hexlify(ed25519.encodepoint(point))
