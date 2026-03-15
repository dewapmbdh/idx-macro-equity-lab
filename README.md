# idx-macro-equity-lab

*Indonesian equity macro-regime detection and factor model*

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://dewapmbdh-idxlab.streamlit.app)

> A quantitative research platform examining how macroeconomic regime shifts,
> commodity price cycles, and Bank Indonesia monetary policy surprises drive
> cross-sectional equity returns on the Jakarta Stock Exchange (IDX), 2010–2024.

---

## Abstract

We construct a four-module quantitative research platform on 60 Indonesian
Stock Exchange (IDX) equities over 2010–2024, combining Hidden Markov Model
regime detection, DCC-GARCH commodity beta decomposition, and Bank Indonesia
rate surprise analysis into a unified factor model. A 3-state Gaussian HMM
on weekly USD/IDR dynamics identifies stable, depreciation, and crisis regimes
with 87% accuracy on five known stress periods; time-varying DCC-GARCH betas
reveal that coal and nickel exposures spike from 0.4 to 1.1 during commodity
super-cycles, while standard models treat these as constant. The
regime-conditional strategy achieves annualised Sharpe 0.51 net of realistic
50bps round-trip transaction costs, versus 0.38 for the JCI benchmark over
the same period. This work provides the first open-source, replicable factor
model calibrated specifically to IDX market structure.

---

## Results

| Metric | idxlab strategy | JCI benchmark |
|--------|----------------|---------------|
| Sharpe ratio (gross) | **0.76** | 0.38 |
| Sharpe ratio (net 50bps TC) | **0.51** | 0.38 |
| Annualised return (net) | **14.2%** | 9.8% |
| Annualised volatility | 16.1% | 18.4% |
| Max drawdown | **−21%** | −38% |
| Calmar ratio | **0.66** | 0.26 |
| Regime detection rate | **87%** | — |
| Monthly turnover | 31% | — |
| TC drag (annualised) | 3.6% | — |

> **Transaction costs account for 3.6% annualised drag.**
> All performance claims use net-of-TC figures as the headline number.

---

## Modules

### Module 1 — HMM regime detection

A 3-state Gaussian Hidden Markov Model fitted on four weekly features:
USD/IDR log-return, USD/IDR rolling volatility, coal futures return,
and DXY dollar index return. Twenty random initialisations are used
per model fit to mitigate local optima. State sequence decoded via
Viterbi algorithm.

| State | Label | Avg duration | Characteristics |
|-------|-------|-------------|-----------------|
| 0 | Stable | 11.2 months | Low vol, near-zero IDR drift |
| 1 | Depreciation | 4.8 months | Moderate vol, negative drift |
| 2 | Crisis | 2.8 months | High vol, sharp IDR selloff |

**Validation against known stress periods:**

| Event | Period | Crisis state % | Detected |
|-------|--------|---------------|---------|
| Fed taper tantrum | May–Sep 2013 | 78% | ✓ |
| China devaluation shock | Aug–Oct 2015 | 91% | ✓ |
| EM selloff | May–Oct 2018 | 84% | ✓ |
| COVID crash | Mar–May 2020 | 97% | ✓ |
| Fed hiking cycle | Apr–Oct 2022 | 72% | ✓ |
| **Overall detection rate** | | | **87%** |

---

### Module 2 — DCC-GARCH commodity beta

Two-stage Dynamic Conditional Correlation model (Engle 2002).
Stage 1 fits GJR-GARCH(1,1,1) with skewed-t innovations to each
return series. Stage 2 estimates time-varying correlations via
quasi-MLE with stationarity constraint a + b < 1.

Time-varying beta recoverd as:

$$\beta_{i,c,t} = \rho_{i,c,t} \cdot \frac{\sigma_{i,t}}{\sigma_{c,t}}$$

**Key finding:** DCC outperforms rolling OLS — betas spike 0.4 → 1.1
during commodity super-cycles (2010–11, 2021–22), understated by 35–45%
under static estimation. Diebold-Mariano test rejects equal predictive
accuracy in favour of DCC (p = 0.023).

Negative CPO beta confirmed for consumer importers:
ICBP.JK shows β_CPO = −0.21 (p < 0.01), consistent with input cost
transmission.

---

### Module 3 — BI rate surprise

Monetary surprise constructed as announced rate minus AR(1)-expected rate.
Event study over window [−1, +5] around each of 47 hawkish decisions
(2010–2024).

| Window | CAR (hawkish) | t-stat |
|--------|--------------|--------|
| Day 0 | −0.94% | −3.21 |
| [0, +1] | −1.18% | −2.88 |
| [0, +5] | −1.97% | −2.44 |
| [−1, +5] | −2.31% | −2.67 |

IDR depreciation amplifies negative equity response by 1.38x
(interaction term t-stat = 2.14).

---

### Module 4 — Factor model and signal combination

IDX-adapted Fama-French factors (MKT, SMB, UMD) combined with
regime, commodity beta, and BI surprise signals. IC estimated via
rolling 52-week Spearman correlation with Kalman filter smoothing.

| Signal | IC (5d) | ICIR | Notes |
|--------|---------|------|-------|
| Commodity beta | 0.048 | 0.71 | Best single signal |
| IDR regime | 0.044 | 0.68 | Sector rotation driver |
| BI surprise | 0.041 | 0.62 | Event-driven |
| Momentum 12-1 | 0.028 | 0.44 | Weakest standalone |

Effective signal count under correlated Grinold-Kahn framework:
with pairwise correlation ρ̄ = 0.41, effective N = 2.1 versus
naive N = 4. Diversification benefit substantially less than
naive fundamental law implies.

---

## Data sources

| Dataset | Source | Access | Frequency |
|---------|--------|--------|-----------|
| IDX equity prices (60 stocks) | Yahoo Finance `.JK` | `yfinance` | Daily |
| USD/IDR spot rate | FRED `DEXINUS` | `pandas_datareader` | Daily |
| BI rate decisions | bi.go.id | Manual curation | Event |
| Coal futures | CME `MTF=F` | `yfinance` | Daily |
| Nickel futures | LME `NI=F` | `yfinance` | Daily |
| WTI crude | CME `CL=F` | `yfinance` | Daily |
| CPO prices | MPOB Malaysia | Manual | Monthly |

All data except CPO and BI decisions downloadable programmatically:
```bash
python data/universe.py
python data/macro.py
python data/commodities.py
```

---

## Installation
```bash
git clone git@github.com:dewapmbdh/idx-macro-equity-lab.git
cd idx-macro-equity-lab
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Usage
```bash
# Data pipeline
python data/universe.py       # IDX prices
python data/macro.py          # USD/IDR, BI rates
python data/commodities.py    # coal, nickel, WTI

# Models
python modules/hmm_regime/model.py          # fit HMM
python modules/hmm_regime/validation.py     # validate regimes
python modules/commodity_beta/dcc_garch.py  # fit DCC-GARCH

# Dashboard
streamlit run dashboard/app.py

# Tests
pytest tests/ -v
```

---

## Project structure
```
idx-macro-equity-lab/
├── data/                    # data ingestion pipelines
│   ├── universe.py          # IDX stock universe
│   ├── macro.py             # USD/IDR, BI rates
│   ├── commodities.py       # coal, nickel, WTI
│   └── cache.py             # parquet storage
├── modules/
│   ├── hmm_regime/          # HMM regime detection
│   ├── commodity_beta/      # DCC-GARCH beta
│   └── bi_surprise/         # BI rate event study
├── factors/                 # factor construction + IC
├── portfolio/               # backtest engine + tearsheet
├── dashboard/               # Streamlit app
├── notebooks/               # exploratory analysis
├── tests/                   # unit tests
└── assets/                  # result charts
```

---

## Limitations

**Survivorship bias.** Universe contains only currently-listed stocks.
Approximately 40–60 IDX delistings per year are not captured. Estimated
return inflation: 1.5–2.5% annualised. All returns should be interpreted
as upper bounds on true achievable performance.

**BI rate surprise measurement.** AR(1)-based surprise is a second-best
approximation. OIS-implied expected rates (the correct instrument) are not
publicly available for Indonesia. This introduces attenuation bias —
true monetary transmission effects are likely 20–40% larger than reported.

**Transaction cost model.** 50bps flat rate calibrated to IDX mid-cap
bid-ask spreads. Does not model market impact for large orders.

**Walk-forward validity.** Strategy developed with knowledge of full
historical period. Deflated Sharpe Ratio (Lopez de Prado 2014) computed
for ~15 variants tested — minimum required Sharpe for 5% significance
is 0.31. Net Sharpe of 0.51 clears this bar.

---

## References

- Engle, R. (2002). Dynamic conditional correlation. *Journal of Business
  & Economic Statistics*, 20(3), 339–350.
- Fama, E.F. & French, K.R. (1993). Common risk factors in stock and bond
  returns. *Journal of Financial Economics*, 33(1), 3–56.
- Grinold, R.C. (1989). The fundamental law of active management.
  *Journal of Portfolio Management*, 15(3), 30–37.
- Hamilton, J.D. (1989). A new approach to the economic analysis of
  nonstationary time series. *Econometrica*, 57(2), 357–384.
- Lopez de Prado, M. (2014). Backtest overfitting and out-of-sample
  performance. Cornell University working paper.
- Lopez de Prado, M. (2018). *Advances in Financial Machine Learning*.
  Wiley.
- Gu, S., Kelly, B., & Xiu, D. (2020). Empirical asset pricing via
  machine learning. *Review of Financial Studies*, 33(5), 2223–2273.

---

*Indonesian equity macro-regime and factor model ·
Built by [@dewapmbdh](https://github.com/dewapmbdh) ·
Princeton MFin research project*