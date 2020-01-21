import hashlib
import base64

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
        content += scriptPubKey(address)
        content += "ffffffff"
   
    ## Outputs 
    content += pack_int(len(outputs), 1)
    for output in outputs:
        content += pack_satoshis_values(value)
        content += scriptPubKey(address)
        content += ""

    ## Locktime
    content += "00000000"
    ## hash code type
    content += "01000000"
    return (content)

def signed_transaction(inputs, outputs):
    first_transaction(inputs, outputs)
    hashed_trans = hashlib.sha256(hashlib.sha256(first_transaction.encode()))

inputs = [
        {'hash' : "HASH", "index" : 0, 'address' : ""}
]

outputs = [
    {'address' : "ADDRESS", 'value' : 0}
]

print(pack_transaction(inputs, outputs))

