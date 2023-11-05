import os
import logging

import requests

ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")

if ETHERSCAN_API_KEY is None:
    logging.error("Etherscan API key is null, exiting now ")
    exit(1)
else:
    logging.debug("Etherscan API Key loaded")

ETHERSCAN_BASE_URL = "https://api.etherscan.io/api"

def convert_wei_to_eth(wei: str) -> str:
    """ Converts a balance in WEI to ETH """
    return str(int(wei) / 1000000000000000000)

def get_eth_balance(address: str) -> str:
    """ Returns eth balance at current block in WEI """
    balance_response = requests.get(f"{ETHERSCAN_BASE_URL}?module=account&action=balance&address={address}&tag=latest&apikey={ETHERSCAN_API_KEY}")

    balance_response_json = balance_response.json()

    if balance_response_json["status"] != '1':
        result = balance_response_json["result"]
        logging.debug(f"Error fetching balance for address {address} -- {result}")
        return "0"
    else:
        return balance_response_json["result"]
    
def get_erc20_balances(address: str) -> dict:
    balance_response = requests.get(f"{ETHERSCAN_BASE_URL}?module=account&action=addresstokenbalance&address={address}&page=1&offset=100&apikey={ETHERSCAN_API_KEY}")
    print(balance_response.json())
