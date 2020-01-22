import hashlib
import struct

b58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

def base58encode(n):
    result = ''
    while n > 0:
        result = b58[n%58] + result
        n = n//58
    return result

def base58decode(s):
    result = 0
    for i in range(0, len(s)):
        result = result * 58 + b58.index(s[i])
    return result

def base256encode(n):
    print("base256 encode, n : ")
    print(n)
    result = ''
    while n > 0:
        result = chr(n % 256) + result
        n = n//256
    return result

def base256decode(s):
    result = 0
    for c in s:
        result = result * 256 + ord(c)
    return result

def countLeadingChars(s, ch):
    count = 0
    for c in s:
        if c == ch:
            count += 1
        else:
            break
    return count

def base58CheckDecode(s):
    leadingOnes = countLeadingChars(s, '1')
    s = base256encode(base58decode(s))
    result = '\0' * leadingOnes + s[:-4]
    chk = s[-4:]

    result = result.encode()
    chk = chk.encode()

    print('chk')
    print(chk)
    checksum = hashlib.sha256(hashlib.sha256(result).digest()).digest()[0:4]
    print('checksum')
    print(checksum)
    assert(chk == checksum)
    version = result[0]
    return result[1:]

def wifToPrivateKey(s):
    b = base58CheckDecode(s)
    return b.encode('hex')
