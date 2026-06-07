import numpy as np

from btc_binary_engine.payoffs import (
    binary_yes_payoff,
    binary_no_payoff,
    fair_binary_price,
)


def test_yes_payoff_single_price_above_strike():
    assert binary_yes_payoff(105000, 100000) == 1.0


def test_yes_payoff_single_price_below_strike():
    assert binary_yes_payoff(95000, 100000) == 0.0


def test_yes_payoff_equal_to_strike_loses():
    assert binary_yes_payoff(100000, 100000) == 0.0


def test_no_payoff_single_price_below_strike():
    assert binary_no_payoff(95000, 100000) == 1.0


def test_payoff_vector_output():
    prices = np.array([95000, 100000, 105000])
    strike = 100000

    expected_yes = np.array([0.0, 0.0, 1.0])
    expected_no = np.array([1.0, 1.0, 0.0])

    np.testing.assert_array_equal(binary_yes_payoff(prices, strike), expected_yes)
    np.testing.assert_array_equal(binary_no_payoff(prices, strike), expected_no)


def test_fair_binary_price():
    assert fair_binary_price(0.65) == 0.65


def test_discounted_fair_binary_price():
    assert fair_binary_price(0.65, discount_factor=0.98) == 0.637


def test_invalid_probability_raises_error():
    try:
        fair_binary_price(1.2)
    except ValueError as error:
        assert "Probability must be between 0 and 1" in str(error)
