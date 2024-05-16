EIP712Domain = [
    {"name": "name", "type": "string"},
    {"name": "version", "type": "string"},
    {"name": "chainId", "type": "uint256"},
    {"name": "verifyingContract", "type": "address"},
]

Order = [
    {"name": "salt", "type": "uint256"},
    {"name": "maker", "type": "address"},
    {"name": "receiver", "type": "address"},
    {"name": "makerAsset", "type": "address"},
    {"name": "takerAsset", "type": "address"},
    {"name": "makingAmount", "type": "uint256"},
    {"name": "takingAmount", "type": "uint256"},
    {"name": "makerTraits", "type": "uint256"},
]

LimitOrderV4TypeDataName = "1inch Aggregation Router"
LimitOrderV4TypeDataVersion = "6"
