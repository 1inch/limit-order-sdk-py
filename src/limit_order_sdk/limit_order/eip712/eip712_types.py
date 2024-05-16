from typing import Dict, List, Union
from dataclasses import dataclass


@dataclass
class EIP712TypedData:
    types: Dict[str, List[Dict[str, str]]]
    domain: Dict[str, Union[str, int, float]]
    message: Dict[str, Union[str, int, float]]
    primaryType: str


@dataclass
class EIP712DomainType:
    name: str
    version: str
    chainId: int
    verifyingContract: str
