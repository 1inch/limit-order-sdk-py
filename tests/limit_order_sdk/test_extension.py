from limit_order_sdk import Extension


def test_extension_encode_decode():
    # Create an instance of Extension with specific data
    ext = Extension(maker_asset_suffix="0x01", taker_asset_suffix="0x02", maker_permit="0x03", predicate="0x04", making_amount_data="0x05", taking_amount_data="0x06", pre_interaction="0x07", post_interaction="0x08", custom_data="0xff")

    # Encode the instance and then decode it back
    decoded_ext = Extension.decode(ext.encode())

    assert ext.maker_asset_suffix == decoded_ext.maker_asset_suffix
    assert ext.taker_asset_suffix == decoded_ext.taker_asset_suffix
    assert ext.maker_permit == decoded_ext.maker_permit
    assert ext.predicate == decoded_ext.predicate
    assert ext.making_amount_data == decoded_ext.making_amount_data
    assert ext.taking_amount_data == decoded_ext.taking_amount_data
    assert ext.pre_interaction == decoded_ext.pre_interaction
    assert ext.post_interaction == decoded_ext.post_interaction
    assert ext.custom_data == decoded_ext.custom_data
