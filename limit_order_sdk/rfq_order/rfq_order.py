from limit_order_sdk.limit_order import LimitOrder, MakerTraits, OrderInfoData
from typing import Dict, Any
from limit_order_sdk.address import Address


class RfqOrder(LimitOrder):
    """
    Light, gas efficient version of LimitOrder.
    It does not support multiple fills and extension.
    """

    def __init__(self, order_info: OrderInfoData, options: Dict[str, Any]):
        allowed_sender = options.get("allowed_sender", None)
        nonce = options["nonce"]  #  Unique id among all maker orders. Max value is UINT_40_MAX
        expiration = options["expiration"]  # Timestamp in seconds

        use_permit2 = options.get("use_permit2", False)
        maker_traits = MakerTraits(0).disable_multiple_fills().allow_partial_fills().with_expiration(expiration).with_nonce(nonce)

        if allowed_sender:
            maker_traits.with_allowed_sender(allowed_sender)

        if use_permit2:
            maker_traits.enable_permit2()

        super().__init__(order_info, maker_traits)
