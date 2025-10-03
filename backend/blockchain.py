# blockchain.py
from web3 import Web3
import json
import os

# Ganache URL
GANACHE_URL = "http://127.0.0.1:8545"
w3 = Web3(Web3.HTTPProvider(GANACHE_URL))

# Get the absolute path to the JSON file
script_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(script_dir, '..', 'blockchain-project', 'build', 'contracts', 'FIRStorage.json')

# Get ABI and Contract Address from your Truffle deployment
with open(json_path) as f:
    contract_json = json.load(f)
    contract_abi = contract_json['abi']
    contract_address = contract_json['networks']['1759330334566']['address'] # 5777 is Ganache's default network ID

contract = w3.eth.contract(address=contract_address, abi=contract_abi)

def store_fir_on_blockchain(case_id: str, ipfs_hash: str, officer_address: str):
    """Stores the FIR's CID on the blockchain."""
    try:
        tx_hash = contract.functions.storeFIR(case_id, ipfs_hash).transact({'from': officer_address})
        return w3.eth.wait_for_transaction_receipt(tx_hash)
    except Exception as e:
        print(f"Blockchain transaction failed: {e}")
        return None

def get_fir_from_blockchain(case_id: str):
    """Retrieves an FIR record from the blockchain."""
    return contract.functions.getFIR(case_id).call()