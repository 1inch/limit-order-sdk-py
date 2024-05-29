from limit_order_sdk import BitMask


def test_should_create_single_bit_mask():
    assert str(BitMask(0)) == "0x1"
    assert str(BitMask(1)) == "0x2"
    assert str(BitMask(16)) == "0x10000"


def test_should_create_multi_bit_mask():
    assert str(BitMask(0, 16)) == "0xffff"
    assert str(BitMask(16, 32)) == "0xffff0000"
    assert str(BitMask(32, 35)) == "0x700000000"
