import pytest
from limit_order_sdk import RfqOrder, OrderInfoData, Address, UINT_40_MAX


def test_should_validate_max_nonce():
    # Testing the creation of an RfqOrder with a nonce exceeding the maximum allowed value
    with pytest.raises(Exception):
        RfqOrder(
            {
                "makerAsset": Address("0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"),
                "takerAsset": Address("0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"),
                "makingAmount": 1000000000000000000,
                "takingAmount": 1420000000,
                "maker": Address("0x00000000219ab540356cbb839cbe05303d7705fa"),
            },
            {"nonce": 1 << 41, "expiration": 1000},
        )


def test_should_create_rfq_order_with_permit2():
    order_info = OrderInfoData(
        maker_asset=Address("0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"),
        taker_asset=Address("0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"),
        making_amount=1000000000000000000,
        taking_amount=1420000000,
        maker=Address("0x00000000219ab540356cbb839cbe05303d7705fa"),
    )
    options = {"nonce": 1, "expiration": 1000, "use_permit2": True}
    order = RfqOrder(order_info, options)

    assert order.maker_traits.is_permit2(), "Permit2 should be enabled"
