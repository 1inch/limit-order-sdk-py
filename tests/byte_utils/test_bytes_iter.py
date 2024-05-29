from limit_order_sdk import BytesIter, Side


def test_iterate_as_int():
    iter = BytesIter.to_int("0xdeadbeef")
    assert iter.next_byte() == 0xDE
    assert iter.next_byte() == 0xAD
    assert iter.next_bytes(2) == 0xBEEF


def test_iterate_as_string():
    iter = BytesIter.string("0xdeadbeef")
    assert iter.next_byte() == "0xde"
    assert iter.next_byte() == "0xad"
    assert iter.next_bytes(2) == "0xbeef"


def test_iterate_in_reverse():
    iter = BytesIter.string("0xdeadbeef")
    assert iter.next_byte(Side.Back) == "0xef"
    assert iter.next_byte(Side.Back) == "0xbe"
    assert iter.next_bytes(2, Side.Back) == "0xdead"
