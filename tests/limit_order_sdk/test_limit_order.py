import pytest
from unittest.mock import patch
from limit_order_sdk import LimitOrder, MakerTraits, ExtensionBuilder, OrderInfoData, Address


@pytest.fixture
def mock_random():
    with patch("random.random", return_value=1):
        yield


@pytest.fixture
def mock_datetime():
    with patch("datetime.datetime") as mock_datetime:
        mock_datetime.now.return_value = 1673549418040
        yield


def test_create_limit_order(mock_random, mock_datetime):
    order_info = OrderInfoData(
        maker_asset=Address("0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"),
        taker_asset=Address("0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"),
        making_amount=1000000000000000000,
        taking_amount=1420000000,
        maker=Address("0x00000000219ab540356cbb839cbe05303d7705fa"),
    )

    order = LimitOrder(order_info=order_info)
    assert LimitOrder.from_calldata(order.to_calldata()) == order


def test_create_limit_order_with_passed_salt(mock_random, mock_datetime):
    order_info = OrderInfoData(
        maker_asset=Address("0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"),
        taker_asset=Address("0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"),
        making_amount=1000000000000000000,
        taking_amount=1420000000,
        maker=Address("0x00000000219ab540356cbb839cbe05303d7705fa"),
        salt=10,
    )

    order = LimitOrder(order_info=order_info)
    assert LimitOrder.from_calldata(order.to_calldata()) == order


def test_create_limit_order_with_extension_and_salt(mock_random, mock_datetime):
    ext = ExtensionBuilder().with_custom_data("0xdeadbeef").build()
    order_info = OrderInfoData(
        maker_asset=Address("0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"),
        taker_asset=Address("0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"),
        making_amount=1000000000000000000,
        taking_amount=1420000000,
        maker=Address("0x00000000219ab540356cbb839cbe05303d7705fa"),
        salt=LimitOrder.build_salt(ext),
    )
    order = LimitOrder(
        order_info=order_info,
        maker_traits=MakerTraits.default(),
        extension=ext,
    )

    assert LimitOrder.from_data_and_extension(order.build(), ext) == order
