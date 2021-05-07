import hashlib
import ecdsa
import codecs
import binascii
import base58
from binascii import hexlify
from base58 import b58encode
import os, sys, time


def random_secret_exponent(curve_order):
    while True:
        bytes = os.urandom(32)
        random_hex = hexlify(bytes)
        random_int = int(random_hex, 16)
        if random_int >= 1 and random_int < curve_order:
            return random_int


def generate_private_key():
    curve = ecdsa.curves.SECP256k1
    se = random_secret_exponent(curve.order)
    from_secret_exponent = ecdsa.keys.SigningKey.from_secret_exponent
    return from_secret_exponent(se, curve, hashlib.sha256).to_string()


def get_public_key_uncompressed(private_key_bytes):
    k = ecdsa.SigningKey.from_string(private_key_bytes, curve=ecdsa.SECP256k1)
    return b'\04' + k.get_verifying_key().to_string()  # 0x04 = uncompressed key prefix


def get_bitcoin_address(public_key_bytes, prefix=b'\x00'):
    ripemd160 = hashlib.new('ripemd160')
    ripemd160.update(hashlib.sha256(public_key_bytes).digest())
    r = prefix + ripemd160.digest()
    checksum = hashlib.sha256(hashlib.sha256(r).digest()).digest()[0:4]
    return b58encode(r + checksum)


def get_wif_format_key(private_key):
    private_key = codecs.encode(private_key, 'hex').decode('utf-8')
    extended_key = "ef" + private_key
    # Step 3: first SHA-256
    first_sha256 = hashlib.sha256(binascii.unhexlify(extended_key)).hexdigest()
    # Step 4: second SHA-256
    second_sha256 = hashlib.sha256(binascii.unhexlify(first_sha256)).hexdigest()
    # Step 5-6: add checksum to end of extended key
    final_key = extended_key+second_sha256[:8]
    # Step 7: finally the Wallet Import Format is the base 58 encode of final_key
    WIF_private_key = base58.b58encode(binascii.unhexlify(final_key))
    return WIF_private_key


prefix = input("Input the prefix you want: ")
while True:
  private_key = generate_private_key()
  wif_key = get_wif_format_key(private_key)
  public_key = get_public_key_uncompressed(private_key)
  address = get_bitcoin_address(public_key)
  if address.decode('utf-8')[1:len(prefix)+1].lower() != prefix.lower():
    print(address.decode('utf-8')[1:len(prefix)+1])
    continue
  
  print("private_key: " + codecs.encode(private_key, 'hex').decode('utf-8'))
  print("base58 private_key: " + base58.b58encode(binascii.unhexlify(codecs.encode(private_key, 'hex').decode('utf-8'))).decode('utf-8'))
  print("WIF key: " + wif_key.decode('utf-8'))
  print("public_key: " + codecs.encode(public_key, 'hex').decode('utf-8'))
  print("address: " + address.decode('utf-8'))
  break
