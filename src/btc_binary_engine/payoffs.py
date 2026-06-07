"""
Binary payoff utilities for BTC YES/NO prediction-market contracts.

The goal of this module is to represent a prediction-market BTC event
as a simple binary financial claim.

Example:
    Will BTC be above 100,000 at expiry?

    YES payoff = 1 if final BTC price > 100,000, otherwise 0.
    NO payoff  = 1 if final BTC price <= 100,000, otherwise 0.
"""

import numpy as np


def binary_yes_payoff(final_price, strike):
    """
    Calculate the payoff of a YES binary contract.

    Parameters
    ----------
    final_price : float or array-like
        BTC price at contract expiry.
    strike : float
        Contract threshold level.

    Returns
    -------
    float or np.ndarray
        1.0 if final_price > strike, otherwise 0.0.
    """
    return np.where(np.asarray(final_price) > strike, 1.0, 0.0)


def binary_no_payoff(final_price, strike):
    """
    Calculate the payoff of a NO binary contract.

    The NO contract is the opposite side of the YES contract.
    It pays 1.0 when the YES contract loses.
    """
    return 1.0 - binary_yes_payoff(final_price, strike)


def fair_binary_price(probability, discount_factor=1.0):
    """
    Convert a model probability into a fair binary contract price.

    In prediction markets, a binary contract price can be interpreted
    as an implied probability. For example, a price of 0.62 means the
    market is roughly pricing the event at 62%.

    Parameters
    ----------
    probability : float
        Estimated probability that the YES event occurs.
    discount_factor : float, optional
        Discount factor applied to the expected payoff.

    Returns
    -------
    float
        Fair binary contract price.
    """
    if probability < 0 or probability > 1:
        raise ValueError("Probability must be between 0 and 1.")

    if discount_factor <= 0:
        raise ValueError("Discount factor must be positive.")

    return probability * discount_factor
