import hashlib
import base64
import ecdsa

import keyUtils

my_address="mji6tgw9ZnrRAXN49uy8y2AXc7M5BGfxRx"
hash_utxo="4be05aaad356e4258bbb85818df836137c1246602cbccecf052f34e989a14865"

private_key_base58check="93UexCJHWp59BXxb2YrixM6NEkMxe7omrGz2mPifQGvQjGtDcuz"
private_key = keyUtils.wifToPrivateKey(private_key_base58check)

recipient_address="n3GNqMveyvaPvUbH469vDRadqpJMPc84JA"
change_address="mji6tgw9ZnrRAXN49uy8y2AXc7M5BGfxRx"

def pack_int(number, bytes_number): 
    format = "%" + str(2*bytes_number) + "s"
    return (format % hex(number)[2:]).replace(" ", "0")

def to_little_endian(hash):
#    return reversed hash
    return hash

def scriptPubKey(address):
    script = "76a9" + address + "88ac"
    script_len = pack_int(len(script), 1)
    return (script_len + script)
    ## OP_DUP OP_HASH <Address> OP_EQUALVERIFY OP_CHECKSIG

def pack_satoshis_values(value):
    return to_little_endian(pack_int(value, 8))

def pack_transaction(inputs, ouputs):
    # Version
    content = "01000000"
    ## Inputs
    content += pack_int(len(inputs), 1)
    content += ("%2s" % hex(len(inputs))[2:]).replace(" ", "0")
    for input in inputs:
        content += to_little_endian(input['hash'])
        content += pack_int(input['index'], 4)
        content += scriptPubKey(input['address'])
        content += "ffffffff"
   
    ## Outputs 
    content += pack_int(len(outputs), 1)
    for output in outputs:
        content += pack_satoshis_values(output['value'])
        content += scriptPubKey(output['address'])
        content += ""

    ## Locktime
    content += "00000000"
    ## hash code type
    content += "01000000"
    return (content)

def signed_transaction(inputs, outputs):
    first_transaction = pack_transaction(inputs, outputs)
    hashed_trans = hashlib.sha256(first_transaction.encode()).hexdigest() #first hash
    hashed_trans = hashlib.sha256(hashed_trans.encode()).hexdigest() #second hash

    sk = ecdsa.SigningKey.from_string(privateKey.decode('hex'), curve=ecdsa.SECP256k1)
#    sk = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1)

    sig = sk.sign_digest(s256, sigencode=ecdsa.util.sigencode_der) + '\01' # 01 is hashtype


    return (sig)


inputs = [
        {'hash' : hash_utxo, "index" : 0, 'address' : my_address}
]

outputs = [
    {'address' : recipient_address, 'value' : 10000},
    {'address' : change_address, 'value' : 145000}
]


my_tx = signed_transaction(inputs, outputs)

print(my_tx)

