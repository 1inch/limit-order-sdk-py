from limit_order_sdk import rand_int


def test_rand_int_range():
    # Beware that due to the nature of randomness, this test may falsely succesed sometimes
    assert rand_int(1) >= 0, "rand_int(1) should be equal to or greater than 0"
    assert rand_int(1) <= 1, "rand_int(1) should be equal to or less than 1"
    assert rand_int(10) >= 0, "rand_int(10) should be equal to or greater than 0"
    assert rand_int(10) <= 10, "rand_int(10) should be equal to or less than 10"

    # For very large numbers, it's better to convert them to int explicitly if they are not already
    big_max = int(2**96)
    random_value = rand_int(big_max)
    assert random_value >= 0, "rand_int(2**96) should be equal to or greater than 0"
    assert random_value <= big_max, f"rand_int(2**96) should be equal to or less than (2**96)"
