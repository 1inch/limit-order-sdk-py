ZX = "0x"

ONE_INCH_LIMIT_ORDER_V4 = "0x111111125421ca6dc452d289314280a0f8842a65"
ONE_INCH_LIMIT_ORDER_V4_ZK_SYNC = "0x6fd4383cb451173d5f9304f041c7bcbf27d561ff"


def get_limit_order_contract(chain_id: int) -> str:
    """
    Returns the correct 1inch limit order contract address based on the chain ID.

    Args:
        chain_id (int): The chain ID for which to get the limit order contract address.

    Returns:
        str: The limit order contract address for the specified chain.
    """
    if chain_id == 324:  # ZkSync
        return ONE_INCH_LIMIT_ORDER_V4_ZK_SYNC

    return ONE_INCH_LIMIT_ORDER_V4
