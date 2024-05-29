from limit_order_sdk import Interaction, Address


def test_interaction_encode_decode():
    interaction = Interaction(Address.from_int(1337), "0xdeadbeef")
    encoded = interaction.encode()
    decoded_interaction = Interaction.decode(encoded)

    assert str(interaction.target) == str(decoded_interaction.target)
    assert interaction.data == decoded_interaction.data
