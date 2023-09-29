#!/usr/bin/python3
#Michael Brown (mjb4us)

# This is the homework submission file for the BTC Scripting homework, which
# can be found at http://aaronbloomfield.github.io/ccc/hws/btcscript.  That
# page describes how to fill in this program.


from bitcoin.wallet import CBitcoinAddress, CBitcoinSecret
from bitcoin import SelectParams
from bitcoin.core import CMutableTransaction
from bitcoin.core.script import *
from bitcoin.core import x


#------------------------------------------------------------
# Do not touch: change nothing in this section!

# ensure we are using the bitcoin testnet and not the real bitcoin network
SelectParams('testnet')

# The address that we will pay our tBTC to -- do not change this!
tbtc_return_address = CBitcoinAddress('mv4rnyY3Su5gjcDNzbMLKBQkBicCtHUtFB') # https://coinfaucet.eu/en/btc-testnet/

# The address that we will pay our BCY to -- do not change this!
bcy_dest_address = CBitcoinAddress('mgBT4ViPjTTcbnLn9SFKBRfGtBGsmaqsZz')

# Yes, we want to broadcast transactions
broadcast_transactions = True

# Ensure we don't call this directly
if __name__ == '__main__':
    print("This script is not meant to be called directly -- call bitcoinctl.py instead")
    exit()


#------------------------------------------------------------
# Setup: your information

# Your UVA userid
userid = 'mjb4us'

# Enter the BTC private key and invoice address from the setup 'Testnet Setup'
# section of the assignment.  
my_private_key_str = "cP7U4yGyq7vPPdKYFhYGowyQooPsxG5nf3PMMfZUNsUZ3dusTXLC"
my_invoice_address_str = "mtu3xpiksnrepRKgce1pGNRTGhqBzqAdYd"

# Enter the transaction ids (TXID) from the funding part of the 'Testnet
# Setup' section of the assignment.  Each of these was provided from a faucet
# call.  And obviously replace the empty string in the list with the first
# one you botain..
txid_funding_list = ["f53f72d701a9419648e64a47bc92f1a3e9018dcb1234133b8dd4f7c07d81f8c0", "d373b4fb7c94c22321abffc2ee37f3f79cd75c9c4c031d14abfcbaaefb03a108", "c1b4594015b3f80c228f5a96f6447bab12318121e956f9d1f19197faa5100985", "38909184c5b9aee3d371dd5b888aa60146d98701bc92b03271ee80118e8e887a"]

# These conversions are so that you can use them more easily in the functions
# below -- don't change these two lines.
if my_private_key_str != "":
    my_private_key = CBitcoinSecret(my_private_key_str)
    my_public_key = my_private_key.pub


#------------------------------------------------------------
# Utility function(s)

# This function will create a signature of a given transaction.  The
# transaction itself is passed in via the first three parameters, and the key
# to sign it with is the last parameter.  The parameters are:
# - txin: the transaction input of the transaction being signed; type: CMutableTxIn
# - txout: the transaction output of the transaction being signed; type: CMutableTxOut
# - txin_scriptPubKey: the pubKey script of the transaction being signed; type: list
# - private_key: the private key to sign the transaction; type: CBitcoinSecret
def create_CHECKSIG_signature(txin, txout, txin_scriptPubKey, private_key):
    tx = CMutableTransaction([txin], [txout])
    sighash = SignatureHash(CScript(txin_scriptPubKey), tx, 0, SIGHASH_ALL)
    return private_key.sign(sighash) + bytes([SIGHASH_ALL])


#------------------------------------------------------------
# Testnet Setup: splitting coins

# The transaction ID that is to be split -- the assumption is that it is the
# transaction hash, above, that funded your account with tBTC.  You may have
# to split multiple UTXOs, so if you are splitting a different faucet
# transaction, then change this appropriately. It must have been paid to the
# address that corresponds to the private key above
txid_split = txid_funding_list[0] #1 and 3 issue.

# After all the splits, you should have around 10 (or more) UTXOs, all for the
# amount specified in this variable. That amount should not be less than
# 0.0001 BTC, and can be greater.  It will make your life easier if each
# amount is a negative power of 10, but that's not required.
split_amount_to_split = 0.01
split_amount_to_split = 0.00005197 #this is for cross chain


# How much BTC is in that UTXO; look this up on https://live.blockcypher.com
# to get the correct amount.
split_amount_after_split = 0.001
split_amount_after_split = 0.000025985 #for cross chain txn

# How many UTXO indices to split it into -- you should not have to change
# this!  Note that it will actually split into one less, and use the last one
# as the transaction fee.
split_into_n = int(split_amount_to_split/split_amount_after_split)

# The transaction IDs obtained after successfully splitting the tBTC.
txid_split_list = ["4381b5b7ac54d2ceb6bf71ca1553ae9225e0063a118818f8949fb949e14a29a2", "9577c7ba8f9e30868bba79f1d753c3ae27c959e5f75f82a10bfe7306118ba89d", "5613918d43480deca3b3fcd04cbab0962c59d84ce6d5a9bca8f7431da67657b9", "2d42da6f3417563324da5218aabe0c1406adcace617ab8c8f59596d8934b9132"]


#------------------------------------------------------------
# Global settings: some of these will need to be changed for EACH RUN

# The transaction ID that is being redeemed for the various parts herein --
# this should be the result of the split transaction, above; thus, the
# default is probably sufficient.
txid_utxo = txid_split_list[0] #was 1 for issue one. and now 3!!!!

# This is likely not needed.  The bitcoinctl.py will take a second
# command-line parmaeter, which will override this value.  You should use the
# second command-line parameter rather than this variable. The index of the
# UTXO that is being spent -- note that these indices are indexed from 0.
# Note that you will have to change this for EACH run, as once a UTXO index
# is spent, it can't be spent again.  If there is only one index, then this
# should be set to 0.
utxo_index = -1

# How much tBTC to send -- this should be LESS THAN the amount in that
# particular UTXO index -- if it's not less than the amount in the UTXO, then
# there is no miner fee, and it will not be mined into a block.  Setting it
# to 90% of the value of the UTXO index is reasonable.  Note that the amount
# in a UTXO index is split_amount_to_split / split_into_n.
send_amount = split_amount_after_split * 0.3
#send_amount = 0.00001 * 0.4

#------------------------------------------------------------
# Part 1: P2PKH transaction

# This defines the pubkey script (aka output script) for the transaction you
# are creating.  This should be a standard P2PKH script.  The parameter is:
# - address: the address this transaction is being paid to; type:
#   P2PKHBitcoinAddress
def P2PKH_scriptPubKey(address):
    #address is hashed public key i believe

    return [OP_DUP, OP_HASH160, address, OP_EQUALVERIFY, OP_CHECKSIG ]

# This function provides the sigscript (aka input script) for the transaction
# that is being redeemed.  This is for a standard P2PKH script.  The
# parameters are:
# - txin: the transaction input of the UTXO being redeemed; type:
#   CMutableTxIn
# - txout: the transaction output of the UTXO being redeemed; type:
#   CMutableTxOut
# - txin_scriptPubKey: the pubKey script (aka output script) of the UTXO being
#   redeemed; type: list
# - private_key: the private key of the redeemer of the UTXO; type:
#   CBitcoinSecret
def P2PKH_scriptSig(txin, txout, txin_scriptPubKey, private_key):
    sig = create_CHECKSIG_signature(txin, txout, txin_scriptPubKey, private_key)

    return [ sig, private_key.pub ]

# The transaction hash received after the successful execution of this part
txid_p2pkh = "a98586953da273cfd4f2a3e25f67af1823b5d87ef421fdbbc57a33022ec10a3f"


#------------------------------------------------------------
# Part 2: puzzle transaction

# These two values are constants that you should choose -- they should be four
# digits long.  They need to allow for only integer solutions to the linear
# equations specified in the assignment.
puzzle_txn_p = 4000
puzzle_txn_q = 6000

# These are the solutions to the linear equations specified in the homework
# assignment.  You can use an online linear equation solver to find the
# solutions.
puzzle_txn_x = 2000
puzzle_txn_y = 2000

# This function provides the pubKey script (aka output script) that requres a
# solution to the above equations to redeem this UTXO.
def puzzle_scriptPubKey():
    #stack after dups -- [x, y, x, y, y]
    return [ 
            OP_2DUP, OP_DUP, OP_ADD, OP_ADD, puzzle_txn_q, OP_EQUALVERIFY, OP_ADD, puzzle_txn_p, OP_EQUALVERIFY, OP_TRUE
           ]

# This function provides the sigscript (aka input script) for the transaction
# that you are redeeming.  It should only provide the two values x and y, but
# in the order of your choice.
def puzzle_scriptSig():
    return [ 
             puzzle_txn_x, puzzle_txn_y
           ]

# The transaction hash received after successfully submitting the first
# transaction above (part 2a)
txid_puzzle_txn1 = "6dac57c6d3bfc385fd7ffb596fe8706319e42a49ea6b1ab87e687e2747670018"
#bfd3d79f96f090dde68ca5248069541c3fcb700383abda124e103a40298e4a04 failed

# The transaction hash received after successfully submitting the second
# transaction above (part 2b)
txid_puzzle_txn2 = "f3f8e7fc856cf5bf4614e4e015c16cfaa4b0f4502f12f3685cadb253afda599f"


#------------------------------------------------------------
# Part 3: Multi-signature transaction

# These are the public and private keys that need to be created for alice,
# bob, and charlie
alice_private_key_str = "cPuABK6PkwCbgSyRLmfv8qKURFr5hhfBRK4JEx3boG4AUzEdCLSc"
alice_invoice_address_str = "mnEVmjgRW7wnjP17asbkxv46xB6YoTbKko"
bob_private_key_str = "cVPhzgLJHUDCb753GReejv6qsmysL5YtuddtdWf1vAEqTK475wNb"
bob_invoice_address_str = "mp5LJmPA4PcDPhLVj3WgN9jtz2gqH7dVKk"
charlie_private_key_str = "cTED9h6WTnrtGnkg7nsFgT1bXQKdKcxi1RBVuTkfXzycpG7ApZph"
charlie_invoice_address_str = "mpc28Hz25QsWE8PXLtndGJ3jowTTYKTZeU"

# These three lines convert the above strings into the type that is usable in
# a script -- you should NOT modify these lines.
if alice_private_key_str != "":
    alice_private_key = CBitcoinSecret(alice_private_key_str)
if bob_private_key_str != "":
    bob_private_key = CBitcoinSecret(bob_private_key_str)
if charlie_private_key_str != "":
    charlie_private_key = CBitcoinSecret(charlie_private_key_str)

# This function provides the pubKey script (aka output script) that will
# require multiple different keys to allow redeeming this UTXO.  It MUST use
# the OP_CHECKMULTISIGVERIFY opcode.  While there are no parameters to the
# function, you should use the keys above for alice, bob, and charlie, as
# well as your own key.
def multisig_scriptPubKey():
    return [
        OP_2, alice_private_key.pub, bob_private_key.pub, charlie_private_key.pub, OP_3, OP_CHECKMULTISIGVERIFY
           ]

# This function provides the sigScript (aka input script) that can redeem the
# above transaction.  The parameters are the same as for P2PKH_scriptSig
# (), above.  You also will need to use the keys for alice, bob, and charlie,
# as well as your own key.  The private key parameter used is the global
# my_private_key.
def multisig_scriptSig(txin, txout, txin_scriptPubKey):
    bank_sig = create_CHECKSIG_signature(txin, txout, txin_scriptPubKey, my_private_key)
    alice_sig = create_CHECKSIG_signature(txin, txout, txin_scriptPubKey, alice_private_key)
    bob_sig = create_CHECKSIG_signature(txin, txout, txin_scriptPubKey, bob_private_key)
    charlie_sig = create_CHECKSIG_signature(txin, txout, txin_scriptPubKey, charlie_private_key)
    return [
        OP_TRUE, OP_0, alice_sig, bob_sig
    ]

# The transaction hash received after successfully submitting the first
# transaction above (part 3a)
txid_multisig_txn1 = "fe13b9a05c3b872cda9b8b0edf5685460a2fa363e7d7c12571057ae1e4871fbe"

# The transaction hash received after successfully submitting the second
# transaction above (part 3b)
txid_multisig_txn2 = "ec394695c532bbbbe9607ce5e1115128ee28822558dfa226d05a228be504cb88"


#------------------------------------------------------------
# Part 4: cross-chain transaction

# This is the API token obtained after creating an account on
# https://accounts.blockcypher.com/.  This is optional!  But you may want to
# keep it here so that everything is all in once place.
blockcypher_api_token = "9cbe127cb91445fdbe72bc7f61ee730e"

# These are the private keys and invoice addresses obtained on the BCY test
# network.
my_private_key_bcy_str = "a9972120f2397b618b835ab43a70e2264cfd595ca2ba8c1346c987fdb8551a1e"
my_invoice_address_bcy_str = "C8NJKTKQmaLavGACyJGaZH2aSPv6wFmbPg"
#bob_private_key_bcy_str = "ba90f683aa99d844a3c1fdaa91757b54ee4245e080eed111935f8d0a3a1b9c62"
#bob_invoice_address_bcy_str = "C5e6ogpqLM7AwaXDdPXDMxMXVRMiLjmNd7"
bob_private_key_bcy_str = "1635ed95dd0c0654af811160d9c1796c2d25c68d786a96f35d39e1829663af15"
bob_invoice_address_bcy_str = "C8DqzsQX7cnnJypVhczyCYzokpajXfsX6D"
#02683c5a330acaa6ab04cdddc285a48767a9c6a59faabe5788443b99ab59ff8afb    public!!

# This is the transaction hash for the funding transaction for Bob's BCY
# network wallet.
#txid_bob_bcy_funding = "f98b3d1149a677d6f75d8cfc1332fc08719633bbbd26912004f9b8dbdd4e136e"
txid_bob_bcy_funding = "21a1b1bdc20dfbbc963b6bf118ab9e4f4f662a2f9debb29ebf82b783a465f022"

# This is the transaction hash for the split transaction for the trasnaction
# above.
# txid_bob_bcy_split = "11ed46b72d0a0b55a071f74aa11b66cab62521f5a1d541ae4c393c259bb24b1e"
txid_bob_bcy_split = "6a7fea38cf25d59a2863b26ab3be8996de8be0eb5de8acc0f75906046d2eea49"


# This is the secret used in this atomic swap.  It needs to be between 1 million
# and 2 billion.
atomic_swap_secret = 17000001

# This function provides the pubKey script (aka output script) that will set
# up the atomic swap.  This function is run by both Alice (aka you) and Bob,
# but on different networks (tBTC for you/Alice, and BCY for Bob).  This is
# used to create TXNs 1 and 3, which are described at
# http://aaronbloomfield.github.io/ccc/slides/bitcoin.html#/xchainpt1.
def atomicswap_scriptPubKey(public_key_sender, public_key_recipient, hash_of_secret):
    return [ 
        #OP_IF, OP_HASH160, hash_of_secret, OP_EQUALVERIFY, public_key_recipient, OP_EQUALVERIFY, OP_ELSE, OP_IF,
        #OP_2, public_key_recipient, public_key_sender, OP_2, OP_CHECKMULTISIGVERIFY, OP_ENDIF


        # OP_IF, OP_HASH160, hash_of_secret, OP_EQUALVERIFY, public_key_recipient, OP_EQUALVERIFY, OP_ELSE, OP_IF,
        # OP_2, public_key_recipient, public_key_sender, OP_2, OP_CHECKMULTISIGVERIFY, OP_ENDIF, OP_ENDIF, OP_TRUE
        # OP_IF, OP_HASH160, hash_of_secret, OP_EQUALVERIFY, public_key_recipient, OP_EQUALVERIFY, OP_ELSE, OP_IF,
        # public_key_sender, OP_EQUALVERIFY, public_key_recipient, OP_EQUALVERIFY, OP_ENDIF, OP_ENDIF, OP_TRUE


        # OP_IF, OP_HASH160, hash_of_secret, OP_EQUALVERIFY, public_key_recipient, OP_EQUALVERIFY, OP_ELSE, OP_IF,
        # public_key_sender, OP_EQUALVERIFY, public_key_recipient, OP_EQUALVERIFY, OP_ENDIF, OP_ENDIF, OP_TRUE

        OP_IF, OP_HASH160, hash_of_secret, OP_EQUALVERIFY, public_key_recipient, OP_CHECKSIGVERIFY, OP_ELSE,
        public_key_sender, OP_CHECKSIGVERIFY, public_key_recipient, OP_CHECKSIGVERIFY, OP_ENDIF, OP_TRUE
           ]

# This is the ScriptSig that the receiver will use to redeem coins.  It's
# provided in full so that you can write the atomicswap_scriptPubKey()
# function, above.  This creates the "normal" redeeming script, shown in steps 5 and 6 at 
# http://aaronbloomfield.github.io/ccc/slides/bitcoin.html#/atomicsteps.
def atomcswap_scriptSig_redeem(sig_recipient, secret):
    return [
        #added op true for after equal verify.
        sig_recipient, secret, OP_TRUE
    ]

# This is the ScriptSig for sending coins back to the sender if unredeemed; it
# is provided in full so that you can write the atomicswap_scriptPubKey()
# function, above.  This is used to create TXNs 2 and 4, which are
# described at
# http://aaronbloomfield.github.io/ccc/slides/bitcoin.html#/xchainpt1.  In
# practice, this would be time-locked in the future -- it would include a
# timestamp and call OP_CHECKLOCKTIMEVERIFY.  Because the time can not be
# known when the assignment is written, and as it will vary for each student,
# that part is omitted.
def atomcswap_scriptSig_refund(sig_sender, sig_recipient):
    return [
        sig_recipient, sig_sender, OP_FALSE
    ]

# The transaction hash received after successfully submitting part 4a
txid_atomicswap_alice_send_tbtc = "c3174ecd255878c8f817950a94beda74c4a8dff8e18966f427796a324068fbbf" #"8f3573be34f9a6befdbdfe9f502c9c8e3e4891df4ff1e15f1b9ef2446931d37a"

#"6a388aa82d2d4b56456ed4566e66db78c7e1c0ad81e0bc0867950848752d2073" #1c46dc3b6a8d9bc1726b9363793c3a3bb2eadd2ee19d361a64a231c5cf0746ca
#2430a001553674dbae7f8c653a3f48bdc37928d860047295a9db522acab5d99a
#229b7f8df0328e3b287b526ae8f5fad33fb9b93d305a74ab989ad3ec1e27ab35
# The transaction hash received after successfully submitting part 4b
txid_atomicswap_bob_send_bcy = "df0bb9f31d4c4e1eb5cc251c2b23d8c5c26b4c09f0c3e17fc77989943efa5e10" #"0c4e8800fd2b5284fa4a73533b34c8face7048c4720c62942a9eb0192d2ea4c4" #"25a17506bbfa418668c5cd2a639734687e6f2659708dcb9320b783b473743fe5" #3d39df26d9a4801a999e3bae051d4304bd4357d6eb76a861efe10d56852f19bd
#bb95fd93eb9e3c46364fb6c8395cd849365a05d26e99719f89356b0573e1d1ea
# The transaction hash received after successfully submitting part 4c
txid_atomicswap_alice_redeem_bcy = "a3cae83b290b34f0fcd048b09e6c43ab44e81babd1f4dcfdc743c658b4d7dadd" #"1d337bbd14d08fc3421a81e6d0adebb8c76874b82479ea67060ff9d0ae1484fe"
#02c9f2e99fa9414af9e6fe94eef28f0863c5145135c0b423ea26dc97f276d78d
# The transaction hash received after successfully submitting part 4d
txid_atomicswap_bob_redeem_tbtc = "5e0bdf6a6b1df0cacad40f5b850b0a89d600746c223f39ec518664e225cce868" #"121df8f43b8f59588044b6aa4c03709975738c2db0bd4e3ecd0080ab9df36346"
#ea6aba107cc41e7303b71f3c4bda22db45e534c49093851d208514e04dc05bd8
#needed to redo parts 4a and 4b if changed pub key script because went sent the script up there before.
#------------------------------------------------------------
# part 5: return everything to the faucet

# nothing to fill in here, as we are going to look at the balance of
# `my_invoice_address_str` to verify that you've completed this part.

#Txns that I did:
#fc438f90eeeb313837e68cad316b4cec24381ee031f431541ea9352f1df97ce2
#d68be64ab4ee43d65fe251e5d6f75e2965a59b64d321e3f9d3bf9267258921d9
#0786d215a012d85eb8053119e0d73561dcff0a33ddd54beb363c7f97578312df
#335c1caecced4a2e6ba0fc99a0e35ae993590943a887d029501f1ce94091e5ed
#