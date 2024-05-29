import pytest
from limit_order_sdk import Address, MakerTraits, UINT_160_MAX, UINT_40_MAX


@pytest.fixture
def default_traits():
    return MakerTraits.default()


def test_allowed_sender(default_traits):
    sender = Address.from_int(1337)
    default_traits.with_allowed_sender(sender).allowed_sender()
    assert default_traits.allowed_sender() == str(sender)[-20:]


def test_nonce(default_traits):
    nonce = 1 << 10
    default_traits.with_nonce(nonce)
    assert default_traits.nonce_or_epoch() == nonce

    big_nonce = 1 << 50
    with pytest.raises(Exception):
        default_traits.with_nonce(big_nonce)


def test_expiration(default_traits):
    expiration = 1000000
    default_traits.with_expiration(expiration)
    assert default_traits.expiration() == expiration


def test_epoch(default_traits):
    series = 100
    epoch = 1
    default_traits.allow_partial_fills().allow_multiple_fills().with_epoch(series, epoch)
    assert default_traits.series() == series
    assert default_traits.nonce_or_epoch() == epoch
    assert default_traits.is_epoch_manager_enabled() == True


def test_extension(default_traits):
    assert not default_traits.has_extension()
    default_traits.with_extension()
    assert default_traits.has_extension()


def test_partial_fills(default_traits):
    assert default_traits.is_partial_fill_allowed()
    default_traits.disable_partial_fills()
    assert not default_traits.is_partial_fill_allowed()
    default_traits.allow_partial_fills()
    assert default_traits.is_partial_fill_allowed()


def test_multiple_fills(default_traits):
    assert not default_traits.is_multiple_fills_allowed()
    default_traits.allow_multiple_fills()
    assert default_traits.is_multiple_fills_allowed()
    default_traits.disable_multiple_fills()
    assert not default_traits.is_multiple_fills_allowed()


def test_pre_interaction(default_traits):
    assert not default_traits.has_pre_interaction()
    default_traits.enable_pre_interaction()
    assert default_traits.has_pre_interaction()
    default_traits.disable_pre_interaction()
    assert not default_traits.has_pre_interaction()


def test_post_interaction(default_traits):
    assert not default_traits.has_post_interaction()
    default_traits.enable_post_interaction()
    assert default_traits.has_post_interaction()
    default_traits.disable_post_interaction()
    assert not default_traits.has_post_interaction()


def test_permit2(default_traits):
    assert not default_traits.is_permit2()
    default_traits.enable_permit2()
    assert default_traits.is_permit2()
    default_traits.disable_permit2()
    assert not default_traits.is_permit2()


def test_native_unwrap(default_traits):
    assert not default_traits.is_native_unwrap_enabled()
    default_traits.enable_native_unwrap()
    assert default_traits.is_native_unwrap_enabled()
    default_traits.disable_native_unwrap()
    assert not default_traits.is_native_unwrap_enabled()


def test_all(default_traits):
    default_traits.with_allowed_sender(Address.from_int(UINT_160_MAX))
    default_traits.allow_partial_fills()
    default_traits.allow_multiple_fills()
    default_traits.with_epoch(UINT_40_MAX, UINT_40_MAX)
    default_traits.with_expiration(UINT_40_MAX)
    default_traits.with_extension()
    default_traits.enable_permit2()
    default_traits.enable_native_unwrap()
    default_traits.enable_pre_interaction()
    default_traits.enable_post_interaction()
    expected_value = "5f800000000000ffffffffffffffffffffffffffffffffffffffffffffffffff"
    assert hex(default_traits.as_int())[2:] == expected_value
