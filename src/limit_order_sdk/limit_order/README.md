## :toolbox: Functions

- [calc_taking_amount](#gear-calc_taking_amount)
- [calc_making_amount](#gear-calc_making_amount)

### :gear: calc_taking_amount

Calculates taker amount by linear proportion.

| Function | Type |
| ---------- | ---------- |
| `calc_taking_amount` | `(swap_maker_amount: int, order_maker_amount: int, order_taker_amount: int) -> int` |

### :gear: calc_making_amount

Calculates maker amount by linear proportion.

| Function | Type |
| ---------- | ---------- |
| `calc_making_amount` | `(swap_taker_amount: int, order_maker_amount: int, order_taker_amount: int) -> int` |

## :factory: Extension

### Methods

- [decode](#gear-decode)
- [default](#gear-default)
- [keccak256](#gear-keccak256)
- [is_empty](#gear-is_empty)
- [encode](#gear-encode)

#### :gear: decode

Decodes the extension from bytes.

| Method | Type |
| ---------- | ---------- |
| `decode` | `(bytes: str) -> Extension` |

#### :gear: default

Returns a default instance of the Extension.

| Method | Type |
| ---------- | ---------- |
| `default` | `() -> Extension` |

#### :gear: keccak256

Computes a keccak256 hash of the extension data.

| Method | Type |
| ---------- | ---------- |
| `keccak256` | `() -> int` |

#### :gear: is_empty

Checks if the extension is empty.

| Method | Type |
| ---------- | ---------- |
| `is_empty` | `() -> bool` |

#### :gear: encode

Encodes the extension into a hex string.

| Method | Type |
| ---------- | ---------- |
| `encode` | `() -> str` |

## :factory: Interaction

### Methods

- [encode](#gear-encode)

#### :gear: encode

Encodes the interaction into a hex string.

| Method | Type |
| ---------- | ---------- |
| `encode` | `() -> str` |

## :factory: ExtensionBuilder

### Methods

- [with_maker_asset_suffix](#gear-with_maker_asset_suffix)
- [with_taker_asset_suffix](#gear-with_taker_asset_suffix)
- [with_making_amount_data](#gear-with_making_amount_data)
- [with_taking_amount_data](#gear-with_taking_amount_data)
- [with_predicate](#gear-with_predicate)
- [with_maker_permit](#gear-with_maker_permit)
- [with_pre_interaction](#gear-with_pre_interaction)
- [with_post_interaction](#gear-with_post_interaction)
- [with_custom_data](#gear-with_custom_data)
- [build](#gear-build)

#### :gear: with_maker_asset_suffix

Sets a suffix for the maker asset.

| Method | Type |
| ---------- | ---------- |
| `with_maker_asset_suffix` | `(suffix: str) -> ExtensionBuilder` |

#### :gear: with_taker_asset_suffix

Sets a suffix for the taker asset.

| Method | Type |
| ---------- | ---------- |
| `with_taker_asset_suffix` | `(suffix: str) -> ExtensionBuilder` |

#### :gear: with_making_amount_data

Specifies the address and data to calculate making amount.

| Method | Type |
| ---------- | ---------- |
| `with_making_amount_data` | `(address: Address, data: str) -> ExtensionBuilder` |

Parameters:

- `address`: Address of the contract to be called.
- `data`: Data to be passed for calculation.

#### :gear: with_taking_amount_data

Specifies the address and data to calculate taking amount.

| Method | Type |
| ---------- | ---------- |
| `with_taking_amount_data` | `(address: Address, data: str) -> ExtensionBuilder` |

Parameters:

- `address`: Address of the contract to be called.
- `data`: Data to be passed for calculation.

#### :gear: with_predicate

Sets a predicate for the extension.

| Method | Type |
| ---------- | ---------- |
| `with_predicate` | `(predicate: str) -> ExtensionBuilder` |

#### :gear: with_maker_permit

Allows specifying a permit for the maker asset.

| Method | Type |
| ---------- | ---------- |
| `with_maker_permit` | `(token_from: Address, permit_data: str) -> ExtensionBuilder` |

#### :gear: with_pre_interaction

Sets a pre-interaction for the extension.

| Method | Type |
| ---------- | ---------- |
| `with_pre_interaction` | `(interaction: Interaction) -> ExtensionBuilder` |

#### :gear: with_post_interaction

Sets a post-interaction for the extension.

| Method | Type |
| ---------- | ---------- |
| `with_post_interaction` | `(interaction: Interaction) -> ExtensionBuilder` |

#### :gear: with_custom_data

Sets custom data for the extension.

| Method | Type |
| ---------- | ---------- |
| `with_custom_data` | `(data: str) -> ExtensionBuilder` |

#### :gear: build

Builds and returns the extension.

| Method | Type |
| ---------- | ---------- |
| `build` | `() -> Extension` |
