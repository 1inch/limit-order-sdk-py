from web3 import Web3
from eth_typing import HexStr
from eth_account.messages import encode_structured_data

from limit_order_sdk.limit_order.eip712.eip712_types import EIP712DomainType, EIP712TypedData
from limit_order_sdk.limit_order import LimitOrderV4Struct
from limit_order_sdk.constants import get_limit_order_contract
from limit_order_sdk.limit_order.eip712.domain import EIP712Domain, LimitOrderV4TypeDataName, LimitOrderV4TypeDataVersion, Order


def get_order_hash(data: EIP712TypedData) -> str:
    # Encode the structured data
    encoded_data = encode_structured_data({"domain": data.domain, "types": data.types, "message": data.message})

    order_hash = Web3.keccak(["bytes"], [encoded_data])
    return order_hash.hex()


def build_order_typed_data(chain_id: int, verifying_contract: str, name: str, version: str, order: LimitOrderV4Struct) -> EIP712TypedData:
    # web3 library expects the order to be a dictionary
    order_dict = order.to_dict()
    types = {"EIP712Domain": EIP712Domain, "Order": Order}
    obj = EIP712TypedData(primaryType="Order", types=types, domain={"name": name, "version": version, "chainId": chain_id, "verifyingContract": verifying_contract}, message=order_dict)
    return obj


def get_domain_separator(name: str, version: str, chainId: int, verifyingContract: str) -> str:
    domain_data = {"name": name, "version": version, "chainId": chainId, "verifyingContract": verifyingContract}
    eip712_domain = {"primaryType": "EIP712Domain", "types": {"EIP712Domain": EIP712Domain}, "domain": domain_data, "message": domain_data}
    encoded_data = encode_structured_data(eip712_domain)
    return Web3.keccak(["bytes"], [encoded_data]).hex()


def get_limit_order_v4_domain(chain_id: int) -> EIP712DomainType:
    obj = EIP712DomainType(name=LimitOrderV4TypeDataName, version=LimitOrderV4TypeDataVersion, chainId=chain_id, verifyingContract=get_limit_order_contract(chain_id))
    return obj
