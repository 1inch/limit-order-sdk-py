from web3 import Web3
import json


def get_contract_web3(contract_abi_path: str):
    web3 = Web3()
    with open(contract_abi_path, "r") as abi_file:
        contract_abi = json.load(abi_file)

    contract = web3.eth.contract(abi=contract_abi)
    return contract
