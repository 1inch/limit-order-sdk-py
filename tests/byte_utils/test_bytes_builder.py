from limit_order_sdk import BytesBuilder, BN


def test_bytes_builder():
    # deadbeef
    beef = BytesBuilder()
    beef.add_byte("0xde")
    beef.add_byte(BN.from_hex("0xad"))
    beef.add_uint16(BN.from_hex("0xbeef"))
    assert beef.as_hex() == "0xdeadbeef"

    # deadc0de
    code = BytesBuilder("0xde")
    code.add_uint24("0xadc0de")
    assert code.as_hex() == "0xdeadc0de"

    # f00dbabe (shout-out to ledger)
    babe = BytesBuilder()
    babe.add_bytes("0xf0")
    babe.add_byte(BN.from_number(0x0D))
    babe.add_uint16(BN(0xBABE))
    assert babe.as_hex() == "0xf00dbabe"


def test_transform_to_hex():
    assert BytesBuilder("0xdeadbeef").as_hex() == "0xdeadbeef"
    assert BytesBuilder("0xdeadbeef").as_hex(False) == "deadbeef"
