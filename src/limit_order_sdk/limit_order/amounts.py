def calc_taking_amount(swap_maker_amount: int, order_maker_amount: int, order_taker_amount: int) -> int:
    """
    Calculates taker amount by linear proportion.

    Returns the ceiled taker amount. This means that the calculation is rounded up to the nearest integer
    to ensure the taker amount is not underestimated.

    See: https://github.com/1inch/limit-order-protocol/blob/23d655844191dea7960a186652307604a1ed480a/contracts/libraries/AmountCalculatorLib.sol#L6

    Args:
        swap_maker_amount (int): The amount the maker provides in the swap.
        order_maker_amount (int): The original amount the maker provided in the order.
        order_taker_amount (int): The original amount the taker is supposed to provide.

    Returns:
        int: The ceiled taker amount.
    """
    return (swap_maker_amount * order_taker_amount + order_maker_amount - 1) // order_maker_amount


def calc_making_amount(swap_taker_amount: int, order_maker_amount: int, order_taker_amount: int) -> int:
    """
    Calculates maker amount by linear proportion.

    Returns the floored maker amount. This ensures that the calculation does not overestimate
    the amount the maker needs to provide.

    See: https://github.com/1inch/limit-order-protocol/blob/23d655844191dea7960a186652307604a1ed480a/contracts/libraries/AmountCalculatorLib.sol#L6

    Args:
        swap_taker_amount (int): The amount the taker provides in the swap.
        order_maker_amount (int): The original amount the maker provided in the order.
        order_taker_amount (int): The original amount the taker is supposed to provide.

    Returns:
        int: The floored maker amount.
    """
    return (swap_taker_amount * order_maker_amount) // order_taker_amount
