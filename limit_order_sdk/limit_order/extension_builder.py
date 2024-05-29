import re
from limit_order_sdk.limit_order import Extension, Interaction
from limit_order_sdk.constants import ZX
from limit_order_sdk.address import Address


class IExtensionBuilder:
    def build(self) -> Extension:
        raise NotImplementedError("Builder classes must implement this method.")


class ExtensionBuilder(IExtensionBuilder):
    def __init__(self):
        self.maker_asset_suffix = ZX
        self.taker_asset_suffix = ZX
        self.making_amount_data = ZX
        self.taking_amount_data = ZX
        self.predicate = ZX
        self.maker_permit = ZX
        self.pre_interaction = ZX
        self.post_interaction = ZX
        self.custom_data = ZX

    def _validate_hex_string(self, value: str) -> bool:
        return bool(re.match(r"^0x[a-fA-F0-9]+$", value))

    def with_maker_asset_suffix(self, suffix: str) -> "ExtensionBuilder":
        assert self._validate_hex_string(suffix), "MakerAssetSuffix must be valid hex string"
        self.maker_asset_suffix = suffix
        return self

    def with_taker_asset_suffix(self, suffix: str) -> "ExtensionBuilder":
        assert self._validate_hex_string(suffix), "TakerAssetSuffix must be valid hex string"
        self.taker_asset_suffix = suffix
        return self

    def with_making_amount_data(self, address: Address, data: str) -> "ExtensionBuilder":
        assert self._validate_hex_string(data), "MakingAmountData must be valid hex string"
        self.making_amount_data = str(address) + data[2:]  # Remove '0x' and concatenate
        return self

    def with_taking_amount_data(self, address: Address, data: str) -> "ExtensionBuilder":
        assert self._validate_hex_string(data), "TakingAmountData must be valid hex string"
        self.taking_amount_data = str(address) + data[2:]  # Remove '0x' and concatenate
        return self

    def with_predicate(self, predicate: str) -> "ExtensionBuilder":
        assert self._validate_hex_string(predicate), "Predicate must be valid hex string"
        self.predicate = predicate
        return self

    def with_maker_permit(self, token_from: Address, permit_data: str) -> "ExtensionBuilder":
        assert self._validate_hex_string(permit_data), "Permit data must be valid hex string"
        self.maker_permit = str(token_from) + permit_data[2:]  # Remove '0x' and concatenate
        return self

    def with_pre_interaction(self, interaction: Interaction) -> "ExtensionBuilder":
        self.pre_interaction = interaction.encode()
        return self

    def with_post_interaction(self, interaction: Interaction) -> "ExtensionBuilder":
        self.post_interaction = interaction.encode()
        return self

    def with_custom_data(self, data: str) -> "ExtensionBuilder":
        assert self._validate_hex_string(data), "Custom data must be valid hex string"
        self.custom_data = data
        return self

    def build(self) -> Extension:
        return Extension(
            maker_asset_suffix=self.maker_asset_suffix,
            taker_asset_suffix=self.taker_asset_suffix,
            making_amount_data=self.making_amount_data,
            taking_amount_data=self.taking_amount_data,
            predicate=self.predicate,
            maker_permit=self.maker_permit,
            pre_interaction=self.pre_interaction,
            post_interaction=self.post_interaction,
            custom_data=self.custom_data,
        )
