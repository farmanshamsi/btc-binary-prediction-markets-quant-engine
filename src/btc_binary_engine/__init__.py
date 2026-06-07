"""
BTC Binary Prediction Markets Quant Engine.

Core package for modelling BTC YES/NO prediction-market contracts
as binary financial claims.
"""

from .payoffs import binary_yes_payoff, binary_no_payoff, fair_binary_price

__all__ = [
    "binary_yes_payoff",
    "binary_no_payoff",
    "fair_binary_price",
]
