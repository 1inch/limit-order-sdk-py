from eth_abi import decode, encode
import eth_utils
from limit_order_sdk.libs.byte_utils import UINT_160_MAX, UINT_256_MAX, is_hex_string, add_0x
from limit_order_sdk.utils.rand_int import rand_int
from limit_order_sdk.address import Address
from limit_order_sdk.limit_order import Extension, LimitOrderV4Struct, OrderInfoData, MakerTraits
from limit_order_sdk.limit_order.eip712 import build_order_typed_data, get_limit_order_v4_domain, get_order_hash


class LimitOrder:
    web3_types = ["uint256", "address", "address", "address", "address", "uint256", "uint256", "uint256"]

    def __init__(self, order_info: OrderInfoData, maker_traits=MakerTraits(0), extension: Extension = Extension.default()):
        self.maker_asset = order_info.maker_asset
        self.taker_asset = order_info.taker_asset
        self.making_amount = order_info.making_amount
        self.taking_amount = order_info.taking_amount
        self.salt = self.verify_salt(order_info.salt or self.build_salt(extension), extension)
        self.maker = order_info.maker
        self.receiver = order_info.receiver if order_info.receiver and not order_info.receiver.equal(order_info.maker) else Address("0x0000000000000000000000000000000000000000")
        self.maker_traits = maker_traits
        self.extension = extension

        assert self.making_amount <= UINT_256_MAX, "making_amount too big"
        assert self.taking_amount <= UINT_256_MAX, "taking_amount too big"

        if not extension.is_empty():
            self.maker_traits.with_extension()

    def __eq__(self, other):
        if not isinstance(other, LimitOrder):
            return False
        return (
            str(self.maker_asset) == str(other.maker_asset)
            and str(self.taker_asset) == str(other.taker_asset)
            and self.making_amount == other.making_amount
            and self.taking_amount == other.taking_amount
            and self.salt == other.salt
            and str(self.maker) == str(other.maker)
            and str(self.receiver) == str(other.receiver)
            and self.maker_traits.as_int() == other.maker_traits.as_int()
        )

    @staticmethod
    def build_salt(extension: Extension, base_salt=rand_int(1 << 96 - 1)) -> int:
        # Build correct salt for order
        #
        # If order has extension - it is crucial to build correct salt
        # otherwise order won't be ever filled
        #
        # @see https://github.com/1inch/limit-order-protocol/blob/7bc5129ae19832338169ca21e4cf6331e8ff44f6/contracts/OrderLib.sol#L153
        if extension.is_empty():
            return base_salt
        return (base_salt << 160) | (extension.keccak256() & UINT_160_MAX)

    @staticmethod
    def verify_salt(salt: int, extension: Extension) -> int:
        assert salt <= UINT_256_MAX, "salt too big"
        if extension.is_empty():
            return salt

        hash_ = salt & UINT_160_MAX
        expected_hash = extension.keccak256() & UINT_160_MAX
        assert hash_ == expected_hash, "invalid salt: lowest 160 bits should be extension hash"
        return salt

    @staticmethod
    def from_calldata(bytes_: str):
        assert is_hex_string(bytes_), "Bytes should be valid hex string with 0x prefix"
        decoded_bytes = eth_utils.decode_hex(bytes_)
        order = decode(LimitOrder.web3_types, decoded_bytes, strict=False)
        order_info = OrderInfoData(salt=int(order[0]), maker=Address(order[1]), receiver=Address(order[2]), maker_asset=Address(order[3]), taker_asset=Address(order[4]), making_amount=int(order[5]), taking_amount=int(order[6]))
        return LimitOrder(order_info, MakerTraits(order[7]))

    @staticmethod
    def from_data_and_extension(data: LimitOrderV4Struct, extension: Extension):
        order_info = OrderInfoData(
            salt=int(data.salt), maker=Address(data.maker), receiver=Address(data.receiver), maker_asset=Address(data.makerAsset), taker_asset=Address(data.takerAsset), making_amount=int(data.makingAmount), taking_amount=int(data.takingAmount)
        )
        return LimitOrder(
            order_info,
            MakerTraits(data.makerTraits),
            extension,
        )

    def to_calldata(self) -> str:
        order: LimitOrderV4Struct = self.build()
        values = [order.salt, order.maker, order.receiver, order.makerAsset, order.takerAsset, order.makingAmount, order.takingAmount, order.makerTraits]
        assert len(self.web3_types) == len(values), "types/values length mismatch when to_calldata()"
        return add_0x(encode(self.web3_types, values).hex())

    def build(self) -> LimitOrderV4Struct:
        return LimitOrderV4Struct(
            makerAsset=str(self.maker_asset),
            takerAsset=str(self.taker_asset),
            makingAmount=int(self.making_amount),
            takingAmount=int(self.taking_amount),
            makerTraits=self.maker_traits.as_int() or 0,
            salt=int(self.salt),
            maker=str(self.maker),
            receiver=str(self.receiver),
        )

    def get_typed_data(self, chain_id: int):
        domain = get_limit_order_v4_domain(chain_id)
        return build_order_typed_data(domain.chainId, domain.verifyingContract, domain.name, domain.version, self.build())

    def get_order_hash(self, chain_id: int) -> str:
        return get_order_hash(self.get_typed_data(chain_id))

    def is_private(self) -> bool:
        return self.maker_traits.is_private()
