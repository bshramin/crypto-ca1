import hashlib
import ecdsa
import codecs
import binascii
import base58
from binascii import hexlify
from base58 import b58encode
from bip32utils import Base58
from bech32 import bech32encode
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


def hash160(x): # Both accepts & returns bytes
    return hashlib.new('ripemd160', hashlib.sha256(x).digest()).digest()


def p2wpkh_in_p2sh_addr(pk, testnet=False):
    """
    Compressed public key (hex string) -> p2wpkh nested in p2sh address. 'SegWit address.'
    """
    # Script sig is just PUSH(20){hash160(cpk)}
    push_20 = bytes.fromhex("0014")
    script_sig = push_20 + hash160(bytes.fromhex(pk))

    # Address is then prefix + hash160(script_sig)
    prefix = b"\xc4" if testnet else b"\x05"
    address = Base58.check_encode(prefix + hash160(script_sig))
    return address


def pubkey_to_bech32(pub, witver: int = 0x00) -> str:
    """https://github.com/bitcoin/bips/blob/master/bip-0141.mediawiki#witness-program"""
    witprog = hash160(pub)
    return bech32encode("bc", witver, witprog)

private_key = generate_private_key()
wif_key = get_wif_format_key(private_key)
public_key = get_public_key_uncompressed(private_key)
address = get_bitcoin_address(public_key)
p2sh_address = p2wpkh_in_p2sh_addr(codecs.encode(public_key, 'hex').decode('utf-8'), testnet=False)
bech32_address = pubkey_to_bech32(public_key)


print("private_key: " + codecs.encode(private_key, 'hex').decode('utf-8'))
print("base58 private_key: " + base58.b58encode(binascii.unhexlify(codecs.encode(private_key, 'hex').decode('utf-8'))).decode('utf-8'))
print("WIF key: " + wif_key.decode('utf-8'))
print("public_key: " + codecs.encode(public_key, 'hex').decode('utf-8'))
print("address: " + address.decode('utf-8'))
print("p2sh_address: " + p2sh_address)
print("bech32_address: " + bech32_address)
