from dataclasses import dataclass
from typing import List, ClassVar, Any
from web3 import Web3
import logging
from limit_order_sdk.libs.byte_utils import BytesIter, trim_0x, is_hex_string, UINT_32_MAX
from limit_order_sdk.constants import ZX

logger = logging.getLogger("gasless-research-logger")


@dataclass
class Extension:
    maker_asset_suffix: str = ZX
    taker_asset_suffix: str = ZX
    making_amount_data: str = ZX
    taking_amount_data: str = ZX
    predicate: str = ZX
    maker_permit: str = ZX
    pre_interaction: str = ZX
    post_interaction: str = ZX
    custom_data: str = ZX

    fields: ClassVar[List[str]] = ["maker_asset_suffix", "taker_asset_suffix", "making_amount_data", "taking_amount_data", "predicate", "maker_permit", "pre_interaction", "post_interaction"]

    def __post_init__(self):
        for key, val in self.__dict__.items():
            assert is_hex_string(val) or val == ZX, f"{key} must be valid hex string"

    @classmethod
    def decode(cls, bytes: str):
        if bytes == ZX:
            return cls.default()

        iter = BytesIter.string(bytes)
        offsets = int(iter.next_uint256(), base=16)
        consumed = 0

        data_dict = {}

        for field in cls.fields:
            offset = offsets & UINT_32_MAX
            bytes_count = offset - consumed
            data_dict[field] = iter.next_bytes(bytes_count)

            consumed += bytes_count
            offsets >>= 32

        data_dict["custom_data"] = iter.rest()

        return cls(**data_dict)

    @classmethod
    def default(cls):
        return cls()

    def keccak256(self) -> int:
        return int(Web3.keccak(text=self.encode()).hex(), base=16)

    def is_empty(self) -> bool:
        all_interactions = self.get_all()
        all_interactions_concat = "".join([trim_0x(i) for i in all_interactions]) + trim_0x(self.custom_data)
        return len(all_interactions_concat) == 0

    def encode(self) -> str:
        all_interactions = self.get_all()
        all_interactions_concat = "".join([trim_0x(attr) for attr in all_interactions]) + trim_0x(self.custom_data)

        cumulative_sum: int = 0
        offsets: List[int] = []
        for interaction in all_interactions:
            interaction_length: int = int(len(interaction) / 2 - 1)
            cumulative_sum += interaction_length
            offsets.append(int(cumulative_sum))

        encoded_offsets = 0
        for i, offset in enumerate(offsets):
            encoded_offsets += offset << (32 * i)

        extension = "0x"
        if all_interactions_concat:
            hex_representation = hex(encoded_offsets)[2:]  # remove 0x after conversion to hex
            extension += hex_representation.zfill(64) + all_interactions_concat

        return extension

    def get_all(self) -> List[str]:
        return [getattr(self, f) for f in self.fields]
