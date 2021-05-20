import bitcoin.wallet
from bitcoin.core import COIN, b2lx, serialize, x, lx, b2x
from utils import *

bitcoin.SelectParams("testnet") # Select the network (testnet or mainnet)
my_private_key = bitcoin.wallet.CBitcoinSecret("92gpofwfthgN6risZNHK87Z7ynaTGXPgcVmgFNP22xEsFHJvHn9") # Private key in WIF format XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
my_public_key = my_private_key.pub
my_address = bitcoin.wallet.P2PKHBitcoinAddress.from_pubkey(my_public_key)
destination_address = bitcoin.wallet.CBitcoinAddress('n2yhmR6LTUwtpYSm5ut39zMAmPiYBfShxN') # Destination address (recipient of the money)


# to condition spending the outputs
def P2PKH_scriptPubKey_out(address):
    ######################################################################
    ## Fill out the operations for P2PKH scriptPubKey                   ##

    return [OP_DUP, OP_HASH160, my_address, OP_EQUALVERIFY, OP_CHECKSIG]


# to condition spending the outputs
def P2PKH_scriptPubKey_in(address):
    ######################################################################
    ## Fill out the operations for P2PKH scriptPubKey                   ##
    script_hash = b'748284390f9e263a4b766a75d0633c50426eb875'
    return [OP_HASH160, script_hash, OP_EQUAL]


# to show that you own the inputs
def P2PKH_scriptSig(txin, txout, txin_scriptPubKey):
    ######################################################################
    ## Fill out the operations for P2PKH scriptSig                      ##

    signature = create_OP_CHECKSIG_signature(txin, txout, txin_scriptPubKey, my_private_key)
    redeem_script = b'5121022afc20bf379bc96a2f4e9e63ffceb8652b2b6a097f63fbee6ecec2a49a48010e2103a767c7221e9f15f870f1ad9311f5ab937d79fcaeee15bb2c722bca515581b4c052ae'
    return [OP_0, signature, redeem_script]


def send_from_P2PKH_transaction(amount_to_send, txid_to_spend, utxo_index,
                                txout_scriptPubKey):
    txout = create_txout(amount_to_send, txout_scriptPubKey)

    txin_scriptPubKey = P2PKH_scriptPubKey_in(my_address)
    txin = create_txin(txid_to_spend, utxo_index)
    txin_scriptSig = P2PKH_scriptSig(txin, txout, txin_scriptPubKey)

    new_tx = create_signed_transaction(txin, txout, txin_scriptPubKey,
                                       txin_scriptSig)

    return broadcast_transaction(new_tx)


if __name__ == '__main__':
    amount_to_send = 0.01
    txid_to_spend = ('7af2d38f4badb05dfb3141fd814f95e6f57505f03ddfa0fd550b11427fa04947') # TxHash of UTXO
    utxo_index = 0 # UTXO index among transaction outputs
    
    ######################################################################

    print(my_address) # Prints your address in base58
    print(my_public_key.hex()) # Print your public key in hex
    print(my_private_key.hex()) # Print your private key in hex
    txout_scriptPubKey = P2PKH_scriptPubKey_out(my_address)
    response = send_from_P2PKH_transaction(amount_to_send, txid_to_spend, utxo_index, txout_scriptPubKey)
    print(response.status_code, response.reason)
    print(response.text) # Report the hash of transaction which is printed in this section result
