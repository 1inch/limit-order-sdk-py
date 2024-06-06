# 1inch Limit Order Protocol v4 SDK

## Installation

### Package manager (Pypi)
```shell
pip install limit-order-sdk
```

### From source
```shell
pip install git+https://github.com/1inch/limit-order-sdk-py.git
```

## Docs
- [Limit Order](limit_order_sdk/limit_order/README.md)
- [Limit Order Contract](limit_order_sdk/limit_order_contract/README.md)

## Usage examples

### Order creation
```python
from eth_account import Account
import time
import math
from limit_order_sdk import Address, OrderInfoData, LimitOrder, MakerTraits

chain_id = 1 # Ethereum

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

print(f"Limit Order signed message: {signed_message}\n")
```
### RFQ Order creation

`RfqOrder` is a light, gas efficient version of LimitOrder, but it does not support multiple fills and extension
Mainly used by market makers
```python
from eth_account import Account
import time
import math
from limit_order_sdk import RfqOrder, rand_int, UINT_40_MAX

chain_id = 1 # Ethereum

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

print(f"RFQ Order signed message: {signed_message}")
```

### API
```python
from limit_order_sdk import Api, FetchProviderConnector, LimitOrder, ApiConfig

config = ApiConfig(
    chain_id=chain_id,
    auth_key="key",  # get it at https://portal.1inch.dev/
    http_connector=FetchProviderConnector(),  # or use any connector which implements `HttpProviderConnector`
)
api = Api(config)
# submit order
order = LimitOrder(...)  # see `Order creation` section
signature = "0x"
api.submit_order(order, signature)

# get order by hash
order_hash = order.get_order_hash(chain_id)
order_info = api.get_order_by_hash(order_hash)

# get orders by maker
orders = api.get_orders_by_maker(order.maker)
```

