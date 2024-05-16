from eth_account import Account
import time
import math
from pprint import pprint
from limit_order_sdk import Address, OrderInfoData


# This is a well-known test private key, do not use it in production
PRIV_KEY = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"


def create_limit_order(chain_id: int):
    from limit_order_sdk import LimitOrder, MakerTraits

    wallet = Account.from_key(PRIV_KEY)

    # Expiration time setup
    expires_in = 120  # 2 minutes in seconds
    expiration = math.floor(time.time() / 1000) + expires_in

    # Creating a LimitOrder
    maker_traits = MakerTraits.default().with_expiration(expiration)
    order_info_data = OrderInfoData(
        maker_asset=Address("0xdac17f958d2ee523a2206206994597c13d831ec7"),
        taker_asset=Address("0x111111111117dc0aa78b770fa6a738034120c302"),
        making_amount=100_000000,
        taking_amount=10_00000000000000000,
        maker=Address(wallet.address),
        # Optional fields like salt or receiver can be added here if necessary
    )
    order = LimitOrder(order_info_data, maker_traits)

    typed_data = order.get_typed_data(chain_id)
    signed_message = Account.sign_typed_data(PRIV_KEY, typed_data.domain, {"Order": typed_data.types["Order"]}, typed_data.message)

    pprint(f"Limit Order signed message: {signed_message}\n")


def create_rfq_order(chain_id: int):
    from limit_order_sdk import RfqOrder, rand_int, UINT_40_MAX

    wallet = Account.from_key(PRIV_KEY)

    expires_in = 120  # 2 minutes in seconds
    expiration = math.floor(time.time() / 1000) + expires_in

    order_info = OrderInfoData(
        maker_asset=Address("0xdac17f958d2ee523a2206206994597c13d831ec7"),
        taker_asset=Address("0x111111111117dc0aa78b770fa6a738034120c302"),
        making_amount=100_000000,  # 100 USDT
        taking_amount=10_00000000000000000,  # 10 1INCH
        maker=Address(wallet.address),
    )
    options = {"allowedSender": Address("0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"), "expiration": expiration, "nonce": rand_int(UINT_40_MAX)}
    order = RfqOrder(order_info=order_info, options=options)

    typed_data = order.get_typed_data(chain_id)
    signed_message = Account.sign_typed_data(PRIV_KEY, typed_data.domain, {"Order": typed_data.types["Order"]}, typed_data.message)

    pprint(f"RFQ Order signed message: {signed_message}")


if __name__ == "__main__":
    chain_id = 1  # Ethereum
    create_limit_order(chain_id)
    create_rfq_order(chain_id)
