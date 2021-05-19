from bitcoin.core.script import OP_RETURN, OP_TRUE
import bitcoin.wallet
from bitcoin.core import COIN, b2lx, serialize, x, lx, b2x
from utils import *

bitcoin.SelectParams("testnet") # Select the network (testnet or mainnet)
my_private_key = bitcoin.wallet.CBitcoinSecret("92gpofwfthgN6risZNHK87Z7ynaTGXPgcVmgFNP22xEsFHJvHn9") # Private key in WIF format XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
my_public_key = my_private_key.pub
my_address = bitcoin.wallet.P2PKHBitcoinAddress.from_pubkey(my_public_key)
destination_address = bitcoin.wallet.CBitcoinAddress('n2yhmR6LTUwtpYSm5ut39zMAmPiYBfShxN') # Destination address (recipient of the money)


# to condition spending the outputs
def P2PKH_scriptPubKey(address):
    ######################################################################
    ## Fill out the operations for P2PKH scriptPubKey                   ##

    return [OP_DUP, OP_HASH160, my_address, OP_EQUALVERIFY, OP_CHECKSIG]


# to condition spending the outputs
def P2PKH_scriptPubKey1(address):
    ######################################################################
    ## Fill out the operations for P2PKH scriptPubKey                   ##

    return [OP_RETURN, "hi".encode()]


# to condition spending the outputs
def P2PKH_scriptPubKey2(address):
    ######################################################################
    ## Fill out the operations for P2PKH scriptPubKey                   ##

    return [OP_TRUE]


# to show that you own the inputs
def P2PKH_scriptSig(txin, txouts, txin_scriptPubKey):
    ######################################################################
    ## Fill out the operations for P2PKH scriptSig                      ##

    signature = create_OP_CHECKSIG_signature_multi_out(txin, txouts, txin_scriptPubKey, my_private_key)

    return [signature, my_public_key]


def send_from_P2PKH_transaction(amounts_to_send, txid_to_spend, utxo_index, txout_scriptPubKeys):
    txouts=[]

    for index, item in enumerate(amounts_to_send):
        txouts.append(create_txout(item, txout_scriptPubKeys[index]))

    txin_scriptPubKey = P2PKH_scriptPubKey(my_address)
    txin = create_txin(txid_to_spend, utxo_index)
    txin_scriptSig = P2PKH_scriptSig(txin, txouts, txin_scriptPubKey)

    new_tx = create_signed_transaction_multi_out(txin, txouts, txin_scriptPubKey,
                                       txin_scriptSig)

    return broadcast_transaction(new_tx)


if __name__ == '__main__':
    amounts_to_send = [0.0001, 0.0005]
    txout_scriptPubKeys = [P2PKH_scriptPubKey1(my_address), P2PKH_scriptPubKey2(my_address)]
    txid_to_spend = ('8a2146202731e367555c1069be3937b2b75c3599382764050cebd0b28c00580d') # TxHash of UTXO
    utxo_index = 1 # UTXO index among transaction outputs
    
    ######################################################################

    print(my_address) # Prints your address in base58
    print(my_public_key.hex()) # Print your public key in hex
    print(my_private_key.hex()) # Print your private key in hex
    
    response = send_from_P2PKH_transaction(amounts_to_send, txid_to_spend, utxo_index, txout_scriptPubKeys)
    print(response.status_code, response.reason)
    print(response.text) # Report the hash of transaction which is printed in this section result
