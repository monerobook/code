import os, sys
from binascii import hexlify, unhexlify
sys.path.append('../libraries')
import utils
import ed25519

def generate_stealth_address(publicViewKey, privateTxKey,  publicSpendKey, index):
    ## multiply r*A
    derivation = utils.generate_key_derivation(publicViewKey, privateTxKey)
    
    ## concatenate index to derivation then hash and reduce
    ## Hs(rA|i)
    scalar = utils.derivation_to_scalar(derivation, index)
    
    ## multiply by base point
    ## Hs(rA|i)G
    sG = ed25519.scalarmultbase(utils.hex2int(scalar))
    
    ## interpret the public spend key as a point on the curve
    pubPoint  = ed25519.decodepoint(unhexlify(publicSpendKey))
    
    ## add the public spend key to the previously calculated point
    ## Hs(rA|i)G + B
    output = ed25519.edwards(pubPoint, sG)

    ## convert the point to a hex encoded public key
    return hexlify(ed25519.encodepoint(output))

## example
print(generate_stealth_address("be90718b250a06b4bcffca6af948240ad6d8951b730a9711f78d4c9decefb4bd", "12b793b002ed168f36c9dc8d13c0e820546359452f67136f03087eb18208710e", "6b48d1c30a640b0b33d0062188df2edd4e6acac7282b215e86701a644a9f70ba", "01"))
