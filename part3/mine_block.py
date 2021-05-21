import binascii
import time
from hashlib import sha256


def SHA256(text):
    return sha256(text.encode("ascii")).hexdigest()


def mine(block_number, transactions, previous_hash, prefix_zeros):
    prefix_str = '0'*prefix_zeros
    nonce = 0
    while True:
        text = str(block_number) + transactions + previous_hash + str(nonce)
        new_hash = SHA256(text)
        nonce += 1
        if new_hash.startswith(prefix_str):
            print(f"Mining was successfull with nonce value:{nonce}")
            return new_hash


if __name__=='__main__':
    coinbase_data = "810196425AminBashiri"
    coinbase_data = binascii.hexlify(coinbase_data.encode())
    wallet_address = "n2yhmR6LTUwtpYSm5ut39zMAmPiYBfShxN"
    previous_block_number = 6425
    previous_block_hash = "000000004d15e01d3ffc495df7bb638c2b35c5b5dd0ba405615f513e3393f0c7"
    # This is not true:
    previous_block_hex = "0100000000000000000000000000000000000000000000000000000000000000000000003ba3edfd7a7b12b27ac72c3e67768f617fc81bc3888a51323a9fb8aa4b1e5e4adae5494dffff7f20020000000101000000010000000000000000000000000000000000000000000000000000000000000000ffffffff4d04ffff001d0104455468652054696d65732030332f4a616e2f32303039204368616e63656c6c6f72206f6e206272696e6b206f66207365636f6e64206261696c6f757420666f722062616e6b73ffffffff0100f2052a01000000434104678afdb0fe5548271967f1a67130b7105cd6a828e03909a67962e0ea1f61deb649f6bc3f4cef38c4f35504e51ec112de5c384df7ba0b8d578a4c702b6bf11d5fac00000000"
    # This is not true:
    coinbase_transaction = "this is the coinbase transaction"
    merkle_root_hash = SHA256(SHA256(coinbase_transaction))
    difficulty=4


    start = time.time()
    print("Mining started")

    new_hash = mine(
        block_number=previous_block_number+1,
        transactions=coinbase_transaction,
        previous_hash=previous_block_hash,
        prefix_zeros=difficulty
    )

    total_time = str((time.time() - start))
    print(f"Mining took: {total_time} seconds")
    print(new_hash)