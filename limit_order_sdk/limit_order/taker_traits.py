from limit_order_sdk.libs.byte_utils import BitMask, BN, add_0x, get_bytes_count, trim_0x
from limit_order_sdk.limit_order import Extension, Interaction
from limit_order_sdk.address import Address
from limit_order_sdk.constants import ZX


class AmountMode:
    """
    Enum to define the amount modes for handling amounts in the fill function.
    - taker: Amount provided to fill function treated as `takingAmount`.
    - maker: Amount provided to fill function treated as `makingAmount`.
    """

    TAKER = "taker"
    MAKER = "maker"


class TakerTraits:
    """
    This class defines TakerTraits, which are used to encode the taker's preferences for an order in a single uint256.

    The TakerTraits are structured as follows:
    High bits are used for flags.
    - 255 bit `_MAKER_AMOUNT_FLAG` - If set, the taking amount is calculated based on making amount, otherwise making amount is calculated based on taking amount.
    - 254 bit `_UNWRAP_WETH_FLAG` - If set, the WETH will be unwrapped into ETH before sending to taker.
    - 253 bit `_SKIP_ORDER_PERMIT_FLAG` - If set, the order skips maker's permit execution.
    - 252 bit `_USE_PERMIT2_FLAG` - If set, the order uses the permit2 function for authorization.
    - 251 bit `_ARGS_HAS_TARGET` - If set, then first 20 bytes of args are treated as receiver address for maker’s funds transfer.
    - 224-247 bits `ARGS_EXTENSION_LENGTH` - The length of the extension calldata in the args.
    - 200-223 bits `ARGS_INTERACTION_LENGTH` - The length of the interaction calldata in the args.
    - 0-184 bits - The threshold amount (the maximum amount a taker agrees to give in exchange for a making amount).
    """

    MAKER_AMOUNT_FLAG = 255
    UNWRAP_WETH_FLAG = 254
    SKIP_ORDER_PERMIT_FLAG = 253
    USE_PERMIT2_FLAG = 252
    ARGS_HAS_RECEIVER = 251
    THRESHOLD_MASK = BitMask(0, 185)
    ARGS_INTERACTION_LENGTH_MASK = BitMask(200, 224)
    ARGS_EXTENSION_LENGTH_MASK = BitMask(224, 248)

    def __init__(self, flag: int, data: dict):
        self.flags = BN(flag)
        self.receiver = data.get("receiver")
        self.extension = data.get("extension")
        self.interaction = data.get("interaction")

    @classmethod
    def default(cls):
        return cls(0, {})

    def get_amount_mode(self):
        return AmountMode.MAKER if self.flags.get_bit(self.MAKER_AMOUNT_FLAG) else AmountMode.TAKER

    def set_amount_mode(self, mode):
        self.flags = self.flags.set_bit(self.MAKER_AMOUNT_FLAG, 1 if mode == AmountMode.MAKER else 0)
        return self

    def is_native_unwrap_enabled(self):
        return self.flags.get_bit(self.UNWRAP_WETH_FLAG) == 1

    def enable_native_unwrap(self):
        self.flags = self.flags.set_bit(self.UNWRAP_WETH_FLAG, 1)
        return self

    def disable_native_unwrap(self):
        self.flags = self.flags.set_bit(self.UNWRAP_WETH_FLAG, 0)
        return self

    def is_order_permit_skipped(self):
        return self.flags.get_bit(self.SKIP_ORDER_PERMIT_FLAG) == 1

    def skip_order_permit(self):
        self.flags = self.flags.set_bit(self.SKIP_ORDER_PERMIT_FLAG, 1)
        return self

    def is_permit2_enabled(self):
        return self.flags.get_bit(self.USE_PERMIT2_FLAG) == 1

    def enable_permit2(self):
        self.flags = self.flags.set_bit(self.USE_PERMIT2_FLAG, 1)
        return self

    def disable_permit2(self):
        self.flags = self.flags.set_bit(self.USE_PERMIT2_FLAG, 0)
        return self

    def set_receiver(self, receiver: Address):
        self.receiver = receiver
        return self

    def remove_receiver(self):
        self.receiver = None
        return self

    def set_extension(self, ext: Extension):
        self.extension = ext
        return self

    def remove_extension(self):
        self.extension = None
        return self

    def set_interaction(self, interaction: Interaction):
        self.interaction = interaction
        return self

    def remove_interaction(self):
        self.interaction = None
        return self

    def set_amount_threshold(self, threshold: int):
        self.flags = self.flags.set_mask(self.THRESHOLD_MASK, threshold)

    def remove_amount_threshold(self):
        self.flags = self.flags.set_mask(self.THRESHOLD_MASK, 0)
        return self

    def encode(self):
        extension_len = get_bytes_count(self.extension.encode()) if self.extension else 0
        interaction_len = get_bytes_count(self.interaction.encode()) if self.interaction else 0
        self.flags = self.flags.set_bit(self.ARGS_HAS_RECEIVER, 1 if self.receiver else 0).set_mask(self.ARGS_EXTENSION_LENGTH_MASK, extension_len).set_mask(self.ARGS_INTERACTION_LENGTH_MASK, interaction_len)

        args = f"{str(self.receiver) if self.receiver else ZX}{trim_0x(self.extension.encode() if self.extension else '')}{trim_0x(self.interaction.encode() if self.interaction else '')}"

        return {"trait": self.flags.value, "args": args}
