from limit_order_sdk.libs.byte_utils import BitMask, BN, add_0x
from limit_order_sdk.address import Address


class MakerTraits:
    """
    This class encodes and decodes maker traits for limit orders, using bitwise operations to store and manage flags and values.

    The MakerTraits type is an uint256, and different parts of the number are used to encode different traits.
    High bits are used for flags
    - 255 bit `NO_PARTIAL_FILLS_FLAG`          - if set, the order does not allow partial fills
    - 254 bit `ALLOW_MULTIPLE_FILLS_FLAG`      - if set, the order permits multiple fills
    - 253 bit                                  - unused
    - 252 bit `PRE_INTERACTION_CALL_FLAG`      - if set, the order requires pre-interaction call
    - 251 bit `POST_INTERACTION_CALL_FLAG`     - if set, the order requires post-interaction call
    - 250 bit `NEED_CHECK_EPOCH_MANAGER_FLAG`  - if set, the order requires to check the epoch manager
    - 249 bit `HAS_EXTENSION_FLAG`             - if set, the order has extension(s)
    - 248 bit `USE_PERMIT2_FLAG`               - if set, the order uses permit2
    - 247 bit `UNWRAP_WETH_FLAG`               - if set, the order requires to unwrap WETH

    Low 200 bits are used for allowed sender, expiration, nonceOrEpoch, and series
    uint80 last 10 bytes of allowed sender address (0 if any)
    uint40 expiration timestamp (0 if none)
    uint40 nonce or epoch
    uint40 series
    """

    # Low 200 bits are used for allowed sender, expiration, nonceOrEpoch, and series
    ALLOWED_SENDER_MASK = BitMask(0, 80)
    EXPIRATION_MASK = BitMask(80, 120)
    NONCE_OR_EPOCH_MASK = BitMask(120, 160)
    SERIES_MASK = BitMask(160, 200)
    NO_PARTIAL_FILLS_FLAG = 255
    ALLOW_MULTIPLE_FILLS_FLAG = 254
    PRE_INTERACTION_CALL_FLAG = 252
    POST_INTERACTION_CALL_FLAG = 251
    NEED_CHECK_EPOCH_MANAGER_FLAG = 250
    HAS_EXTENSION_FLAG = 249
    USE_PERMIT2_FLAG = 248
    UNWRAP_WETH_FLAG = 247

    def __init__(self, value=0):
        self.value = BN(value)

    @classmethod
    def default(cls):
        """Returns a default MakerTraits with all flags and fields unset."""
        return cls()

    def allowed_sender(self):
        """Extracts and returns the last 10 bytes of the allowed sender address."""
        sender = self.value.get_mask(self.ALLOWED_SENDER_MASK).value
        return hex(sender)[2:].zfill(20)

    def is_private(self):
        """Checks if the order is private (specific allowed sender)."""
        return self.value.get_mask(self.ALLOWED_SENDER_MASK).value != 0

    def with_allowed_sender(self, sender: Address):
        """Sets the allowed sender address for the order."""
        last_half = add_0x(str(sender)[-20:])
        self.value = self.value.set_mask(self.ALLOWED_SENDER_MASK, int(last_half, 16))
        return self

    def with_any_sender(self):
        """Removes the sender restriction, allowing any sender."""
        self.value = self.value.set_mask(self.ALLOWED_SENDER_MASK, 0)
        return self

    def expiration(self):
        """Returns the expiration timestamp or None if no expiration is set."""
        expiration = self.value.get_mask(self.EXPIRATION_MASK).value
        return None if expiration == 0 else expiration

    def with_expiration(self, expiration: int):
        """Sets the expiration timestamp for the order."""
        self.value = self.value.set_mask(self.EXPIRATION_MASK, expiration)
        return self

    def nonce_or_epoch(self):
        """Returns the nonce or epoch, depending on the order configuration."""
        return self.value.get_mask(self.NONCE_OR_EPOCH_MASK).value

    def with_nonce(self, nonce: int):
        """Sets the nonce for the order."""
        self.value = self.value.set_mask(self.NONCE_OR_EPOCH_MASK, nonce)
        return self

    def with_epoch(self, series: int, epoch: int):
        """Sets the epoch and series for the order."""
        self.set_series(series)
        self.enable_epoch_manager_check()
        return self.with_nonce(epoch)

    def series(self):
        """Returns the current series of the order."""
        return self.value.get_mask(self.SERIES_MASK).value

    def has_extension(self):
        """Checks if the order has an extension."""
        return self.value.get_bit(self.HAS_EXTENSION_FLAG) == 1

    def with_extension(self):
        """Marks the order as having an extension."""
        self.value = self.value.set_bit(self.HAS_EXTENSION_FLAG, 1)
        return self

    def has_pre_interaction(self) -> bool:
        """
        Returns True if maker has pre-interaction and False otherwise.
        """
        return self.value.get_bit(self.PRE_INTERACTION_CALL_FLAG) == 1

    def enable_pre_interaction(self) -> "MakerTraits":
        """
        Enable maker pre-interaction.
        """
        self.value = self.value.set_bit(self.PRE_INTERACTION_CALL_FLAG, 1)
        return self

    def disable_pre_interaction(self) -> "MakerTraits":
        """
        Disable maker pre-interaction.
        """
        self.value = self.value.set_bit(self.PRE_INTERACTION_CALL_FLAG, 0)
        return self

    def has_post_interaction(self) -> bool:
        """
        Returns True if maker has post-interaction and False otherwise.
        """
        return self.value.get_bit(self.POST_INTERACTION_CALL_FLAG) == 1

    def enable_post_interaction(self) -> "MakerTraits":
        """
        Enable maker post-interaction.
        """
        self.value = self.value.set_bit(self.POST_INTERACTION_CALL_FLAG, 1)
        return self

    def disable_post_interaction(self) -> "MakerTraits":
        """
        Disable maker post-interaction.
        """
        self.value = self.value.set_bit(self.POST_INTERACTION_CALL_FLAG, 0)
        return self

    def is_epoch_manager_enabled(self) -> bool:
        """
        Returns True if epoch manager check is required.
        """
        return self.value.get_bit(self.NEED_CHECK_EPOCH_MANAGER_FLAG) == 1

    def enable_epoch_manager_check(self) -> None:
        """
        Enable checking against the epoch manager. This is only possible when both partial fills and multiple fills are allowed.
        """
        assert not self.is_bit_invalidator_mode(), "Epoch manager allowed only when partial fills and multiple fills are enabled"
        self.value = self.value.set_bit(self.NEED_CHECK_EPOCH_MANAGER_FLAG, 1)

    def set_series(self, series: int) -> None:
        """
        Set the series number, which is a subgroup for epochs.
        """
        self.value = self.value.set_mask(self.SERIES_MASK, series)

    def is_partial_fill_allowed(self) -> bool:
        """
        Returns True if partial fills are allowed for the order, False otherwise.
        """
        return self.value.get_bit(self.NO_PARTIAL_FILLS_FLAG) == 0

    def allow_partial_fills(self) -> "MakerTraits":
        """
        Allow partial fills for the order.
        """
        self.value = self.value.set_bit(self.NO_PARTIAL_FILLS_FLAG, 0)
        return self

    def disable_partial_fills(self) -> "MakerTraits":
        """
        Disable partial fills for the order.
        """
        self.value = self.value.set_bit(self.NO_PARTIAL_FILLS_FLAG, 1)
        return self

    def is_multiple_fills_allowed(self) -> bool:
        """
        Returns True if multiple fills are allowed for the order, False otherwise.
        """
        return self.value.get_bit(self.ALLOW_MULTIPLE_FILLS_FLAG) == 1

    def allow_multiple_fills(self) -> "MakerTraits":
        """
        Allow the order to be filled multiple times.
        """
        self.value = self.value.set_bit(self.ALLOW_MULTIPLE_FILLS_FLAG, 1)
        return self

    def disable_multiple_fills(self) -> "MakerTraits":
        """
        Restrict the order to only one fill.
        """
        self.value = self.value.set_bit(self.ALLOW_MULTIPLE_FILLS_FLAG, 0)
        return self

    def enable_permit2(self):
        """Enables the use of permit2 for transferring maker funds to the contract."""
        self.value = self.value.set_bit(self.USE_PERMIT2_FLAG, 1)
        return self

    def disable_permit2(self):
        self.value = self.value.set_bit(self.USE_PERMIT2_FLAG, 0)
        return self

    def is_permit2(self) -> bool:
        """
        Returns true if `permit2` enabled for maker funds transfer
        @see https://github.com/Uniswap/permit2
        """
        return self.value.get_bit(self.USE_PERMIT2_FLAG) == 1

    def is_native_unwrap_enabled(self) -> bool:
        return self.value.get_bit(self.UNWRAP_WETH_FLAG) == 1

    def enable_native_unwrap(self):
        """Enables the unwrapping of WRAPPED tokens to NATIVE before sending to the maker."""
        self.value = self.value.set_bit(self.UNWRAP_WETH_FLAG, 1)
        return self

    def disable_native_unwrap(self):
        self.value = self.value.set_bit(self.UNWRAP_WETH_FLAG, 0)
        return self

    def as_int(self) -> int:
        """Returns the current value as an integer."""
        return self.value.value

    def is_bit_invalidator_mode(self) -> bool:
        return not (self.is_partial_fill_allowed() and self.is_multiple_fills_allowed())

    def __str__(self):
        """Returns a string representation of the MakerTraits."""
        return f"MakerTraits(value={self.value})"
