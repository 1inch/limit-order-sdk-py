from web3 import Web3
from web3.contract import Contract
from eth_typing import HexStr
import os

from limit_order_sdk.constants import ZX
from limit_order_sdk.utils import get_contract_web3
from limit_order_sdk.limit_order import TakerTraits, LimitOrderV4Struct


path = os.path.join(os.path.dirname(__file__), "AggregationRouterV6.abi.json")
lop_contract: Contract = get_contract_web3(path)


class LimitOrderContract:
    """
    Class to handle operations related to Limit Order Contracts.
    """

    @staticmethod
    def get_fill_order_calldata(order: LimitOrderV4Struct, signature: str, taker_traits: TakerTraits, amount: int) -> str:
        """
        Fill order WITHOUT an extension and taker interaction.

        :param order: LimitOrderV4Struct, order details.
        :param signature: str, cryptographic signature.
        :param taker_traits: TakerTraits, encoded traits of the taker.
        :param amount: int, amount to fill.
        :return: str, calldata for the fillOrder function.
        """
        r, vs = Web3.to_bytes(hexstr=HexStr(signature[:66])), Web3.to_bytes(hexstr=HexStr("0x" + signature[66:]))
        args, trait = taker_traits.encode()

        assert args == ZX, "takerTraits contains args data, use LimitOrderContract.get_fill_order_args_calldata method"

        return lop_contract.encodeABI(fn_name="fillOrder", args=[order, r, vs, amount, trait])

    @staticmethod
    def get_fill_contract_order_calldata(order: LimitOrderV4Struct, signature: str, taker_traits: TakerTraits, amount: int) -> str:
        """
        Fill contract order (order maker is a smart contract) WITHOUT an extension and taker interaction.

        :param order: LimitOrderV4Struct, order details.
        :param signature: str, cryptographic signature.
        :param taker_traits: TakerTraits, encoded traits of the taker.
        :param amount: int, amount to fill.
        :return: str, calldata for the fillContractOrder function.
        """
        args, trait = taker_traits.encode()

        assert args == ZX, "takerTraits contains args data, use LimitOrderContract.get_fill_contract_order_args_calldata method"

        return lop_contract.encodeABI(fn_name="fillContractOrder", args=[order, signature, amount, trait, args])

    @staticmethod
    def get_fill_order_args_calldata(order: LimitOrderV4Struct, signature: str, taker_traits: TakerTraits, amount: int) -> str:
        """
        Fill order WITH an extension or taker interaction.

        :param order: LimitOrderV4Struct, order details.
        :param signature: str, cryptographic signature.
        :param taker_traits: TakerTraits, encoded traits of the taker.
        :param amount: int, amount to fill.
        :return: str, calldata for the fillOrderArgs function.
        """
        r, vs = Web3.to_bytes(hexstr=HexStr(signature[:66])), Web3.to_bytes(hexstr=HexStr("0x" + signature[66:]))
        args, trait = taker_traits.encode()

        return lop_contract.encodeABI(fn_name="fillOrderArgs", args=[order, r, vs, amount, trait, args])

    @staticmethod
    def get_fill_contract_order_args_calldata(order: LimitOrderV4Struct, signature: str, taker_traits: TakerTraits, amount: int) -> str:
        """
        Fill contract order (order maker is a smart contract) WITH an extension or taker interaction.

        :param order: LimitOrderV4Struct, order details.
        :param signature: str, cryptographic signature.
        :param taker_traits: TakerTraits, encoded traits of the taker.
        :param amount: int, amount to fill.
        :return: str, calldata for the fillContractOrderArgs function.
        """
        args, trait = taker_traits.encode()

        return lop_contract.encodeABI(fn_name="fillContractOrderArgs", args=[order, signature, amount, trait, args])
