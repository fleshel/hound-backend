import os
import logging
import binascii

import requests
from web3 import Web3

ALCHEMY_API_KEY = os.getenv("ALCHEMY_API_KEY")

# setup basic logging, to file and console
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),  # Specify the file to log to
        logging.StreamHandler()  # Log to console
    ]
)

#exit if no alchemy apikey found
if ALCHEMY_API_KEY is not None:
    logging.info("API Key found..")
else:
    logging.critical("API KEY not found, exiting..")
    exit(1)

API_URL = f"https://eth-mainnet.g.alchemy.com/v2/{ALCHEMY_API_KEY}"

REQUEST_HEADERS = {
    "accept": "application/json",
    "content-type": "application/json"
}

def load_erc20_for_address(address: str) -> dict:
    """ 
    Load all ERC-20 tokens owned by an address.
    Returned as dict in format `{contractAddress: tokenBalance}`
    """
    payload = {
        "id": 1,
        "jsonrpc": "2.0",
        "method": "alchemy_getTokenBalances",
        "params": [address, "erc20"]
    }

    response = requests.post(API_URL, json=payload, headers=REQUEST_HEADERS)

    response_statuscode = response.status_code

    if response_statuscode != 200:
        logging.error(f"Alchemy API request failed, status code = {response_statuscode}")
        return {}

    tokens = response.json()['result']['tokenBalances']
    result_dict =  {contract['contractAddress']: int(contract['tokenBalance'][2:], 16) / pow(10, 18) for contract in tokens}

    return result_dict
