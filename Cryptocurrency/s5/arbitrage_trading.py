import arbitrage_config

from web3 import Web3
from hexbytes import HexBytes
import math

w3 = ""

#"local" --- this is geth.ipc way
if arbitrage_config.config.get('connection_is_ipc') == True:

    w3 = Web3(Web3.IPCProvider(arbitrage_config.config.get('connection_uri')))
else:
    #"course server way" --- get data from accessing his site then accessing a geth node...
    w3 = Web3(Web3.WebsocketProvider('wss://andromeda.cs.virginia.edu/geth'))

from web3.middleware import geth_poa_middleware
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

# if (w3.is_connected()):
#     print("connected")
#     #print(w3.eth.get_block('latest'))
# else:
#     print("Not connected")


#after connecting (way of getting same data), arbitrage trade


#find current holdings
eth_balance = w3.eth.get_balance(arbitrage_config.config.get('account_address')) #check -- may be web3.
eth_balance = eth_balance / (10**18)
#print("Eth balance IN ETHER??", eth_balance)

token_addr = arbitrage_config.config.get('tokencc_addr')


contract = w3.eth.contract(address=token_addr, abi=arbitrage_config.itokencc_abi)

#figure out if there's a profit to trade with each dex that i connect to
token_balance = contract.functions.balanceOf(arbitrage_config.config.get('account_address')).call()
token_balance = token_balance / (10 ** contract.functions.decimals().call())

price_eth = arbitrage_config.config.get('price_eth')
price_t = arbitrage_config.config.get('price_tc')

holdings = eth_balance * price_eth + token_balance * price_t
# print("HOLDINGS:", holdings)


f = 1 - arbitrage_config.config.get('dex_fees')


#TRACK THE
is_best_trade_eth = ('', 0, True)     #one element list. Format is [dex_addr, amountTrade, bool ]
                    #if bool is true, trade ether amount.
                    #if false, then trade token.
best_profit = 0
cur_holdings = holdings

decimals = contract.functions.decimals().call()
final_dex_fee = 0

for dex in arbitrage_config.config.get('dex_addrs'):
    #print("DEX:", dex)

    #get dex info
    contractDex = w3.eth.contract(address=dex, abi=arbitrage_config.idex_abi)
    x = contractDex.functions.x().call() / (10 ** 18)
    y = contractDex.functions.y().call() / (10 ** decimals)
    k = contractDex.functions.k().call() / ((10 ** decimals) * (10**18))



    #print("DEX BEFORE TXN", dex)

    # transaction = {
    #     'nonce': w3.eth.get_transaction_count(arbitrage_config.config.get('account_address')),
    #     'from': arbitrage_config.config.get('account_address'),
    #     'to': dex,
    #     'value': w3.to_wei(1, 'ether'),
    #     'chainId': arbitrage_config.config.get('chainId'),
    #     'gas': 170000,
    #     'gasPrice': w3.to_wei(arbitrage_config.config.get('gas_price'), 'gwei')
    # }
    # signed_txn = w3.eth.account.sign_transaction(transaction, private_key=arbitrage_config.config.get('account_private_key'))
    # print("TXN DICT")
    # print(transaction)
    #
    # gas_fees = w3.eth.estimate_gas(transaction)
    # print("GAS FEES ETH TRADE:", gas_fees)


    #determine max optimum val to send ether and token cc
    #Compute both forms for all dex...
    # print("X is :", x)
    # print("y is :", y)
    # print("k is :", k)



    delta_t = -y + math.sqrt(f * k * price_eth / price_t)
    # print("Delta T before decimals raise", delta_t)
    #delta_t = delta_t * (10 ** decimals)  #transfers are going to need to be uints


    delta_e = -x + math.sqrt(f * k * price_t / price_eth)

    # COMPUTER H AFTER ---
    if (delta_t > 0):
        #print("Delta T before comp to token bal:", delta_t)
        if delta_t > token_balance:
            delta_t = token_balance

        if delta_t > arbitrage_config.config.get('max_tc_to_trade'):
            delta_t = arbitrage_config.config.get('max_tc_to_trade')

        #delta_t = delta_t * (10**decimals)
        #print("Delta T:", delta_t)
        #delta_t = int(delta_t)
        #w3.to_checksum_address(
        # transaction = contract.functions.transfer(dex, delta_t).build_transaction({
        #     'gas': 1000000,
        #     'gasPrice': w3.to_wei(arbitrage_config.config.get('gas_price'), 'gwei'),
        #     'from': arbitrage_config.config.get('account_address'),
        #     'nonce': w3.eth.get_transaction_count(arbitrage_config.config.get('account_address'))
        #     # 'chainId': arbitrage_config.config.get('chainId')
        # })
        #
        # gas_fees = w3.eth.estimate_gas(transaction)
        gas_fees = 124000 / (10**18) #must be in ether for equation
        #print("CHECK GAS FEES IN ETHER??", gas_fees)
        # try:
        #     gas_fees = w3.eth.estimate_gas(transaction)  # todo fix
        # except Exception as e:
        #     print("HERE")
        #     print(e)


        hold_after_trade_tc = ( eth_balance + (f * x) - (f * k / (y + delta_t)) ) * price_eth + ((token_balance - delta_t) * price_t) - (gas_fees * price_eth)
        not_withheld_dex_fee = ( eth_balance + (x) - (k / (y + delta_t)) ) * price_eth + ((token_balance - delta_t) * price_t) - (gas_fees * price_eth)
        #print("holding trade tc", hold_after_trade_tc)
        if (holdings < hold_after_trade_tc ):
            cur_profit = hold_after_trade_tc - holdings
            if (cur_profit > best_profit):
                #made better profit with this one. choose this.
                best_profit = cur_profit
                is_best_trade_eth = (dex, delta_t * (10 ** decimals), False)
                cur_holdings = hold_after_trade_tc #not rly used
                final_dex_fee = (not_withheld_dex_fee - hold_after_trade_tc) * arbitrage_config.config.get('dex_fees')


    if (delta_e > 0):
        if delta_e > eth_balance:
            #dont got enough eth, lower to amount i have and see if profitable
            delta_e = eth_balance

        if delta_e > arbitrage_config.config.get('max_eth_to_trade'):

            delta_e = arbitrage_config.config.get('max_eth_to_trade')
        #print("Delta E: ", delta_e)
        # delta_e = delta_e - (200000 / 10**18)
        #delta_e = delta_e - (60000 / (10**18))

        # transaction = {
        #     'nonce': w3.eth.get_transaction_count(arbitrage_config.config.get('account_address')),
        #     'from': arbitrage_config.config.get('account_address'),
        #     'to': dex,
        #     'value': w3.to_wei(delta_e, 'ether'),
        #     'chainId': arbitrage_config.config.get('chainId'),
        #     'gas': 170000,
        #     'gasPrice': w3.to_wei(arbitrage_config.config.get('gas_price'), 'gwei')
        # }
        #
        # gas_fees = w3.eth.estimate_gas(transaction)
        gas_fees = 181000 / (10**18) #must be in ether for equation
        #print("CHECK GAS FEES IN ETHER??", gas_fees)

        hold_after_trade_eth = ( token_balance + f * y - (f * k / (x + delta_e) ) ) * price_t + (eth_balance - delta_e) * price_eth - gas_fees * price_eth
        not_withheld_dex_fee = ( token_balance + y - (k / (x + delta_e) ) ) * price_t + (eth_balance - delta_e) * price_eth - gas_fees * price_eth

        #print("Hold after ETH TRADE", hold_after_trade_eth)
        if (holdings < hold_after_trade_eth):
            cur_profit = hold_after_trade_eth - holdings

            if (cur_profit > best_profit):
                #made better profit with this. track this one
                best_profit = cur_profit
                is_best_trade_eth = (dex, delta_e, True)
                cur_holdings = hold_after_trade_eth #not rly used

                final_dex_fee = (not_withheld_dex_fee - hold_after_trade_eth) * arbitrage_config.config.get('dex_fees')





#At this point, the best option should be found
#if best profit > 0, make a move
if best_profit > 0:
    #print("Final trade", is_best_trade_eth)

    #Determine if i trade ether or tokens
    if is_best_trade_eth[2] == True:
        #print("trading eth")
        #trade eth to dex
        transaction = {
            'nonce': w3.eth.get_transaction_count(arbitrage_config.config.get('account_address')),
            'from': arbitrage_config.config.get('account_address'),
            'to': is_best_trade_eth[0],
            'value': w3.to_wei(is_best_trade_eth[1], 'ether'),
            'chainId': arbitrage_config.config.get('chainId'),
            'gas': 181000,
            'gasPrice': w3.to_wei(arbitrage_config.config.get('gas_price'), 'gwei')
        }
        signed_txn = w3.eth.account.sign_transaction(transaction, private_key=arbitrage_config.config.get('account_private_key'))
        ret = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        w3.eth.wait_for_transaction_receipt(ret)
        #print(w3.eth.get_transaction(ret))

        #Compute new holdings
        new_eth_balance = w3.eth.get_balance(arbitrage_config.config.get('account_address'))  # check -- may be web3.
        new_eth_balance = new_eth_balance / (10 ** 18)

        new_token_balance = contract.functions.balanceOf(arbitrage_config.config.get('account_address')).call()
        new_token_balance = new_token_balance / (10 ** contract.functions.decimals().call())

        final_holdings = new_eth_balance * price_eth + new_token_balance * price_t
        total_fees = 181000 / (10**18)
        total_fees += final_dex_fee


        arbitrage_config.output(-1* is_best_trade_eth[1], new_token_balance - token_balance, total_fees, final_holdings)


    else:
        #print("trading token cc")
        #trade token cc to dex
        #print("DEBUG: ", is_best_trade_eth[1])
        transaction = contract.functions.transfer(is_best_trade_eth[0], int(is_best_trade_eth[1])).build_transaction({
            'gas': 1000000,
            'gasPrice': w3.to_wei(arbitrage_config.config.get('gas_price'), 'gwei'),
            'from': arbitrage_config.config.get('account_address'),
            'nonce': w3.eth.get_transaction_count(arbitrage_config.config.get('account_address')),
            'chainId': arbitrage_config.config.get('chainId')
        })
        signed_txn = w3.eth.account.sign_transaction(transaction, private_key=arbitrage_config.config.get('account_private_key'))
        ret = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        w3.eth.wait_for_transaction_receipt(ret)
        #print(w3.eth.get_transaction(ret))

        # Compute new holdings
        new_eth_balance = w3.eth.get_balance(arbitrage_config.config.get('account_address'))  # check -- may be web3.
        new_eth_balance = new_eth_balance / (10 ** 18)

        new_token_balance = contract.functions.balanceOf(arbitrage_config.config.get('account_address')).call()
        new_token_balance = new_token_balance / (10 ** contract.functions.decimals().call())

        final_holdings = new_eth_balance * price_eth + new_token_balance * price_t
        total_fees = 124000 / (10 ** 18)
        total_fees += final_dex_fee
        #print("FINAL DEX FEE WITHOUT GAS", final_dex_fee)

        arbitrage_config.output(new_eth_balance - eth_balance, -1*is_best_trade_eth[1] / (10 ** decimals), total_fees,
                                final_holdings)
else:
    arbitrage_config.output(0, 0, 0, holdings)

#arbitrage_config.output(ethAmt, tcAmt, fees, holdings)