from bitcoin.core.script import OP_0, OP_2, OP_3, OP_CHECKMULTISIG, OP_TRUE
import bitcoin.wallet
from bitcoin.core import COIN, b2lx, serialize, x, lx, b2x
from utils import *

bitcoin.SelectParams("testnet") # Select the network (testnet or mainnet)
my_private_key = bitcoin.wallet.CBitcoinSecret("92gpofwfthgN6risZNHK87Z7ynaTGXPgcVmgFNP22xEsFHJvHn9") # Private key in WIF format XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
my_public_key = my_private_key.pub
my_address = bitcoin.wallet.P2PKHBitcoinAddress.from_pubkey(my_public_key)
destination_address = bitcoin.wallet.CBitcoinAddress('n2yhmR6LTUwtpYSm5ut39zMAmPiYBfShxN') # Destination address (recipient of the money)
multisig_pvkey_1 = bitcoin.wallet.CBitcoinSecret("92FHLNyScGtzYxyqRGsAVGRzNpkZRM8WwFmsJWfMKxvStRcVsar")
multisig_pvkey_2 = bitcoin.wallet.CBitcoinSecret("92uf7gUfecuwyxoY5P6H6iTGinv3b9LWkt7iQUYTSFmAc9prcdn")
multisig_pvkey_3 = bitcoin.wallet.CBitcoinSecret("91y3y4A8cTdxLK4FA82SfMb67fY1RW5MSEhzxV8CHE7BF4THNJt")
multisig_pubkey_1 = multisig_pvkey_1.pub
multisig_pubkey_2 = multisig_pvkey_2.pub
multisig_pubkey_3 = multisig_pvkey_3.pub


# to condition spending the outputs
def P2PKH_scriptPubKey(address):
    ######################################################################
    ## Fill out the operations for P2PKH scriptPubKey                   ##

    return [OP_DUP, OP_HASH160, my_address, OP_EQUALVERIFY, OP_CHECKSIG]


# to condition spending the outputs
def P2PKH_scriptPubKey_out(address):
    ######################################################################
    ## Fill out the operations for P2PKH scriptPubKey                   ##

    return [OP_2, multisig_pubkey_1, multisig_pubkey_2, multisig_pubkey_3, OP_3, OP_CHECKMULTISIG]


# to show that you own the inputs
def P2PKH_scriptSig(txin, txout, txin_scriptPubKey):
    ######################################################################
    ## Fill out the operations for P2PKH scriptSig                      ##

    signature = create_OP_CHECKSIG_signature(txin, txout, txin_scriptPubKey, my_private_key)

    return [signature, my_public_key]


def send_from_P2PKH_transaction(amount_to_send, txid_to_spend, utxo_index,
                                txout_scriptPubKey):
    txout = create_txout(amount_to_send, txout_scriptPubKey)

    txin_scriptPubKey = P2PKH_scriptPubKey(my_address)
    txin = create_txin(txid_to_spend, utxo_index)
    txin_scriptSig = P2PKH_scriptSig(txin, txout, txin_scriptPubKey)

    new_tx = create_signed_transaction(txin, txout, txin_scriptPubKey,
                                       txin_scriptSig)

    return broadcast_transaction(new_tx)


if __name__ == '__main__':
    amount_to_send = 0.012
    txid_to_spend = ('989eac875a862893c46d0d115ad8c5021428b6afe0262e1d127e1f0fef4fb465') # TxHash of UTXO
    utxo_index = 0 # UTXO index among transaction outputs
    
    ######################################################################

    print(my_address) # Prints your address in base58
    print(my_public_key.hex()) # Print your public key in hex
    print(my_private_key.hex()) # Print your private key in hex
    txout_scriptPubKey = P2PKH_scriptPubKey_out(my_address)
    response = send_from_P2PKH_transaction(amount_to_send, txid_to_spend, utxo_index, txout_scriptPubKey)
    print(response.status_code, response.reason)
    print(response.text) # Report the hash of transaction which is printed in this section result
