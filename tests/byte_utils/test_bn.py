from limit_order_sdk import BN, BitMask


def test_clear_mask():
    bn = BN(0xAB7F1111)
    mask = BitMask(16, 24)

    assert bn.clear_mask(mask).value == 0xAB001111


def test_set_bit():
    bn = BN(0xAB7F1111)

    assert bn.set_bit(0, 0).value == 0xAB7F1110
    assert bn.set_bit(4, 0).value == 0xAB7F1101

    assert bn.set_bit(1, 1).value == 0xAB7F1113
    assert bn.set_bit(5, 1).value == 0xAB7F1131
