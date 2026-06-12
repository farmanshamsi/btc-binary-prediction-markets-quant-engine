# BTC Binary Prediction Markets Quant Engine

A Python-based quant research project for modelling **Bitcoin binary prediction-market contracts** using payoff logic, implied probabilities, machine-learning forecasts, and backtesting.

The project treats a BTC prediction-market contract as a **binary financial claim**:

> Will BTC finish above a specified level by expiry?

The goal is not only to predict whether BTC goes up or down, but to compare a model-derived probability against the market-implied probability and identify whether a contract is overpriced, underpriced, or fairly priced.

---

## Project Motivation

Prediction markets quote event contracts between 0 and 1.

A contract trading at `0.62` can be interpreted as the market assigning roughly a **62% probability** to the event occurring.

For a BTC binary market, the event may look like:

> BTC will be above 100,000 USD at expiry.

This project builds a research engine around that idea:

1. Define the binary payoff.
2. Convert market prices into implied probabilities.
3. Build a BTC directional probability model.
4. Compare model probability with market probability.
5. Backtest whether the model produces positive expected value.
6. Add risk controls before thinking about execution.

---

## Contract Structure

Let:

* ( S_T ) = BTC price at expiry
* ( K ) = contract threshold / strike level
* ( T ) = expiry time
* ( I(\cdot) ) = indicator function

The YES contract pays:

$$
\text{YES Payoff} = I(S_T > K)
$$

Meaning:

$$
\text{YES Payoff} =
\begin{cases}
1, & \text{if } S_T > K \
0, & \text{if } S_T \leq K
\end{cases}
$$

The NO contract is the opposite side:

$$
\text{NO Payoff} = 1 - I(S_T > K)
$$

So:

$$
\text{NO Payoff} =
\begin{cases}
0, & \text{if } S_T > K \
1, & \text{if } S_T \leq K
\end{cases}
$$

This is similar to a cash-or-nothing binary option, but applied to a prediction-market setting.

---

## Market-Implied Probability

If a YES contract trades at price ( P_{\text{YES}} ), then the market-implied probability is approximately:

$$
q_{\text{market}} \approx P_{\text{YES}}
$$

For example:

| YES Price | Market-Implied Probability |
| --------: | -------------------------: |
|      0.35 |                        35% |
|      0.50 |                        50% |
|      0.72 |                        72% |

In a frictionless binary market, the fair value of a YES contract can be written as:

$$
V_{\text{YES}} = D(T) \cdot \mathbb{P}(S_T > K)
$$

where:

* ( D(T) ) is the discount factor
* ( \mathbb{P}(S_T > K) ) is the probability that the event resolves YES

For short-dated prediction markets, the discount factor is often close to 1, so:

$$
V_{\text{YES}} \approx \mathbb{P}(S_T > K)
$$

---

## Model Probability vs Market Probability

The central research question is:

> Is my model probability meaningfully different from the market-implied probability?

Let:

* ( p_{\text{model}} ) = probability estimated by the model
* ( q_{\text{market}} ) = probability implied by the market price

The estimated edge is:

$$
\text{Edge} = p_{\text{model}} - q_{\text{market}}
$$

Interpretation:

| Condition                                      | Interpretation              |
| ---------------------------------------------- | --------------------------- |
| ( p_{\text{model}} > q_{\text{market}} )       | YES may be underpriced      |
| ( p_{\text{model}} < q_{\text{market}} )       | YES may be overpriced       |
| ( p_{\text{model}} \approx q_{\text{market}} ) | Market may be fairly priced |

Example:

If the market prices YES at `0.58`, but the model estimates the true probability as `0.67`, then:

$$
\text{Edge} = 0.67 - 0.58 = 0.09
$$

The model suggests a 9 percentage point edge before fees, slippage, liquidity limits, and model error.

---

## Expected Value

For a YES contract bought at price ( c ), the expected value is:

$$
EV_{\text{YES}} = p_{\text{model}} \cdot (1 - c) - (1 - p_{\text{model}}) \cdot c
$$

This simplifies to:

$$
EV_{\text{YES}} = p_{\text{model}} - c
$$

So if:

* Model probability = `0.64`
* YES price = `0.55`

Then:

$$
EV_{\text{YES}} = 0.64 - 0.55 = 0.09
$$

This means the trade has an estimated positive expected value of 9 cents per contract before costs.

For a NO contract:

$$
EV_{\text{NO}} = (1 - p_{\text{model}}) - c_{\text{NO}}
$$

---

## Machine Learning Framing

The BTC prediction task can be framed as a binary classification problem.

Define the target variable:

$$
y_t =
\begin{cases}
1, & \text{if } S_{t+h} > K_t \
0, & \text{if } S_{t+h} \leq K_t
\end{cases}
$$

where:

* ( S_t ) is the current BTC price
* ( S_{t+h} ) is the BTC price at the prediction horizon
* ( h ) is the forecast horizon
* ( K_t ) is the binary market threshold

The model estimates:

$$
p_{\text{model}} = \mathbb{P}(y_t = 1 \mid X_t)
$$

where ( X_t ) may include:

* BTC returns
* Realized volatility
* Momentum indicators
* Volume
* Trend features
* Funding / derivatives data
* Order book features
* Prediction-market prices
* Market-implied probabilities

---

## Model Evaluation

Accuracy alone is not enough for this project.

A model can be 51% accurate and still lose money if it buys overpriced contracts. A model can also be less accurate but profitable if it only trades when the probability edge is large.

Important evaluation metrics include:

### Classification Metrics

* Accuracy
* Precision
* Recall
* F1-score
* Confusion matrix

### Probability Metrics

* Log loss
* Brier score
* Calibration curve

The Brier score is useful because the model outputs probabilities:

$$
\text{Brier Score} = \frac{1}{N} \sum_{i=1}^{N}(p_i - y_i)^2
$$

where:

* ( p_i ) is the predicted probability
* ( y_i ) is the actual binary outcome

Lower Brier score means better probability forecasting.

### Trading Metrics

* Expected value per trade
* Realized PnL
* Hit rate
* Average win / average loss
* Maximum drawdown
* Sharpe ratio
* Return after fees and slippage

---

## Backtesting Logic

A simple trading rule can be:

$$
\text{Trade YES if } p_{\text{model}} - q_{\text{market}} > \theta
$$

where ( \theta ) is a minimum edge threshold.

For example:

* Model probability = 0.66
* Market probability = 0.58
* Edge threshold = 0.05

Since:

$$
0.66 - 0.58 = 0.08 > 0.05
$$

the engine would mark the YES contract as a potential trade.

The threshold is important because small edges can disappear due to:

* Fees
* Bid-ask spread
* Poor liquidity
* Slippage
* Model error
* Regime changes

---

## Risk Management

This project will include risk controls before treating any signal as tradable.

Possible controls:

* Maximum position size per market
* Maximum total exposure
* Minimum liquidity requirement
* Minimum model confidence
* Minimum edge threshold
* Stop trading after drawdown limit
* Avoid trades near expiry if spreads are too wide

A simple position sizing rule may be based on fractional Kelly sizing:

$$
f^* = \frac{bp - q}{b}
$$

where:

* ( f^* ) = fraction of capital to allocate
* ( b ) = net odds received
* ( p ) = model probability of winning
* ( q = 1 - p )

Because full Kelly can be aggressive, the project will focus on fractional Kelly or capped sizing.

---

## Current Project Status

The project is being built incrementally through small commits.

Current components:

* Binary YES payoff function
* Binary NO payoff function
* Fair binary price helper
* Basic unit tests for payoff logic
* Python package structure using `src/`
* Pytest configuration

---

## Planned Roadmap

### Phase 1 — Contract and Pricing Foundation

* Binary payoff engine
* YES/NO payoff tests
* Market-implied probability helpers
* Bid/ask midpoint logic
* Spread and liquidity cost functions

### Phase 2 — BTC Data Pipeline

* Historical BTC price loader
* Return calculation
* Volatility features
* Momentum features
* Event labelling for binary outcomes

### Phase 3 — Baseline Forecasting Model

* Logistic regression model
* Random forest / gradient boosting model
* Probability calibration
* Feature importance analysis

### Phase 4 — Market vs Model Edge

* Compare model probability with market-implied probability
* Calculate expected value
* Rank opportunities by edge
* Add trade/no-trade decision rules

### Phase 5 — Backtesting and Risk

* Historical simulation
* PnL curve
* Drawdown analysis
* Position sizing
* Risk-adjusted performance metrics

### Phase 6 — Research Dashboard

* Signal dashboard
* Probability comparison chart
* Backtest summary
* Risk report
* Model diagnostics

---

## Repository Structure

```text
btc-binary-prediction-markets-quant-engine/
│
├── src/
│   └── btc_binary_engine/
│       ├── __init__.py
│       └── payoffs.py
│
├── tests/
│   └── test_payoffs.py
│
├── pyproject.toml
├── README.md
├── LICENSE
└── .gitignore
```

---

## Running Tests

Install dependencies:

```bash
python3 -m pip install numpy pytest
```

Run tests:

```bash
python3 -m pytest
```

Expected result:

```text
8 passed
```

---

## Why This Project Matters

Prediction markets are not only about guessing outcomes. They are probability markets.

This project is designed to show the full quant workflow:

1. Convert an event into a financial payoff.
2. Estimate event probability using data.
3. Compare model probability with market price.
4. Trade only when expected value is positive.
5. Backtest the logic.
6. Add risk controls.

The long-term goal is to build a research-grade BTC prediction-market engine that combines:

* Quant finance
* Binary derivatives
* Python engineering
* Machine learning
* Crypto market structure
* Risk management

---

## Disclaimer

This project is for research and educational purposes only.

It is not financial advice, trading advice, or a recommendation to trade prediction markets, cryptocurrencies, or derivatives.
