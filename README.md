# BTC Prediction Markets Quant Engine

### Polymarket-Style YES/NO Pricing, Market-Implied Probabilities, Order Book Signals, ML Forecasting, Risk Controls & Backtesting

This project is a market-specific quant research engine for BTC prediction markets. It treats BTC YES/NO contracts as binary financial claims and estimates the fair probability of an event using CQF-style stochastic modelling, Monte Carlo simulation, financial machine learning, market-implied probabilities, order book signals, and risk-managed backtesting.

The core research question is:

> Can a hybrid quant model combining stochastic simulation, market microstructure data, machine learning, and risk controls identify mispriced BTC binary-event contracts relative to prediction-market prices?

---

## Project Status

This repository is currently under development.

The goal is to build the project incrementally through clear commits:

- Market definition and binary payoff structure
- BTC market data pipeline
- Prediction-market order book data pipeline
- CQF-style Monte Carlo probability model
- ML probability forecasting model
- Market-implied probability comparison
- Edge-based signal generation
- Backtesting with spread, slippage, and liquidity constraints
- Risk management and position sizing

---

## Market Idea

Prediction-market BTC contracts can be viewed as binary outcome claims.

Example contract:

> Will BTC be above a specified level at expiry?

The payoff is binary:

$$
\text{Payoff}_T =
\begin{cases}
1, & S_T > K \\
0, & S_T \leq K
\end{cases}
$$

Where:

- $S_T$ = BTC price at expiry  
- $K$ = contract threshold / strike level  
- Payoff = 1 if the YES contract wins  
- Payoff = 0 if the YES contract loses  

This makes the contract similar to a cash-or-nothing binary option.

---

## Core Quant Framework

The project follows a simple but powerful quant structure:

```text
Binary Event → Probability Estimate → Fair Price → Market Comparison → Signal → Risk-Controlled Backtest
