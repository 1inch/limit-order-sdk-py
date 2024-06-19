from dataclasses import dataclass, asdict
from typing import Optional
from limit_order_sdk.limit_order import Extension
from limit_order_sdk.address import Address


@dataclass
class OrderInfoData:
    maker_asset: Address
    taker_asset: Address
    making_amount: int
    taking_amount: int
    maker: Address
    salt: Optional[int] = None
    receiver: Optional[Address] = None


@dataclass
class LimitOrderV4Struct:
    salt: int
    maker: str
    receiver: str
    makerAsset: str
    takerAsset: str
    makingAmount: int
    takingAmount: int
    makerTraits: int

    def to_dict(self) -> dict:
        """Convert the dataclass to a dictionary"""
        return asdict(self)

    def to_int_tuple(self) -> tuple:
        return (
            self.salt,
            int(self.maker, 16),
            int(self.receiver, 16),
            int(self.makerAsset, 16),
            int(self.takerAsset, 16),
            self.makingAmount,
            self.takingAmount,
            self.makerTraits
        )


class IExtensionBuilder:
    def build(self) -> Extension:
        raise NotImplementedError("This method should be overridden by subclasses.")
