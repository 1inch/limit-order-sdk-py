## :factory: LimitOrderContract

### Methods

- [get_fill_order_calldata](#gear-get_fill_order_calldata)
- [get_fill_contract_order_calldata](#gear-get_fill_contract_order_calldata)
- [get_fill_order_args_calldata](#gear-get_fill_order_args_calldata)
- [get_fill_contract_order_args_calldata](#gear-get_fill_contract_order_args_calldata)

#### :gear: get_fill_order_calldata

Fill order WITHOUT an extension and taker interaction

| Method | Type |
| ---------- | ---------- |
| `get_fill_order_calldata` | `(order: LimitOrderV4Struct, signature: str, taker_traits: TakerTraits, amount: int) => str` |

#### :gear: get_fill_contract_order_calldata

Fill contract order (order maker is smart-contract) WITHOUT an extension and taker interaction

| Method | Type |
| ---------- | ---------- |
| `get_fill_contract_order_calldata` | `(order: LimitOrderV4Struct, signature: str, taker_traits: TakerTraits, amount: int) => str` |

#### :gear: get_fill_order_args_calldata

Fill order WITH an extension or taker interaction

| Method | Type |
| ---------- | ---------- |
| `get_fill_order_args_calldata` | `(order: LimitOrderV4Struct, signature: str, taker_traits: TakerTraits, amount: int) => str` |

#### :gear: get_fill_contract_order_args_calldata

Fill contract order (order maker is smart-contract) WITH an extension or taker interaction

| Method | Type |
| ---------- | ---------- |
| `get_fill_contract_order_args_calldata` | `(order: LimitOrderV4Struct, signature: str, taker_traits: TakerTraits, amount: int) => str` |
