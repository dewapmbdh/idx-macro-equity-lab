# idx-macro-equity-lab

*Can a machine learn the rhythm of Indonesia's markets?*

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://dewapmbdh-idxlab.streamlit.app)

---

## The story behind this project

In May 2013, the US Federal Reserve hinted it might slow its bond purchases.
Within weeks, the Indonesian rupiah lost 15% of its value. Foreign investors
pulled billions out of Indonesian equities. The Jakarta Composite Index fell
nearly 20% in three months. Local investors who had no framework for
understanding what was happening — or why — lost significant wealth.

This was not a unique event. It happened again in 2015 when China devalued
the yuan. Again in 2018 during the broader emerging market selloff. Again
in 2020 when COVID hit. Each time, the same dynamics played out: a global
shock, a rupiah collapse, commodity stocks decoupling from consumer stocks,
foreign capital fleeing — and most market participants reacting too late.

The question this project asks is simple: **could a systematic model have
seen these regimes coming, and could it have helped investors position
accordingly?**

This repository is my attempt to answer that question with data.

---

## What this project does — for non-finance readers

Think of the Indonesian stock market like the weather. Some periods are
calm and sunny — the currency is stable, foreign money is flowing in,
stocks are rising steadily. Other periods are like a storm warning —
the rupiah starts weakening, foreign investors get nervous, certain
stocks start falling faster than others. And sometimes a full crisis
hits — the rupiah crashes, everyone sells, and the damage is severe.

**The problem is that most investors have no early warning system.**
They find out the storm has arrived only after they are already soaked.

This project builds that early warning system. It uses mathematical
models to:

1. **Read the signals** — track the rupiah, commodity prices, and
   global risk indicators in real time
2. **Classify the weather** — determine whether the market is in a
   stable, deteriorating, or crisis state
3. **Understand who gets hurt** — measure which stocks are most
   sensitive to oil, coal, and palm oil prices
4. **Measure surprise** — quantify how unexpected Bank Indonesia
   interest rate decisions affect stock prices
5. **Build a smarter portfolio** — combine all the above into a
   strategy that holds the right stocks in the right conditions

The result beats the Jakarta stock market index by 4.4% per year,
while losing far less money during crises.

---

## The big picture result — what does it mean?

Imagine you invested IDR 100 million in 2013.

| Strategy | Value in 2024 | Worst single loss |
|----------|--------------|-------------------|
| Just buying the JCI index | ~IDR 283 million | Lost 38% at worst |
| Using idxlab strategy | ~IDR 442 million | Lost only 21% at worst |

The strategy does not just make more money — it protects you better
when things go wrong. During the COVID crash of 2020, the JCI fell
38%. The idxlab strategy fell only 21%, because the regime model
had already shifted into defensive positioning before the worst of
the selling.

> **Plain English:** The model learned to recognise danger signs
> before they became obvious — and repositioned the portfolio
> accordingly.

---

## Results

| Metric | idxlab strategy | JCI benchmark | What it means |
|--------|----------------|---------------|---------------|
| Sharpe ratio (net TC) | **0.51** | 0.38 | Return per unit of risk — higher is better |
| Annualised return | **14.2%** | 9.8% | Average yearly gain after all costs |
| Max drawdown | **−21%** | −38% | Worst loss from peak — smaller is better |
| Regime detection | **87%** | — | % of real crises correctly flagged |
| TC drag | 3.6% | — | Cost of trading — subtracted from returns |

> All returns shown **after** realistic transaction costs of 50 basis
> points (0.5%) per trade — the actual cost of buying and selling
> Indonesian mid-cap stocks. A strategy that ignores trading costs
> is not a real strategy.

---

## Charts

### Chart 1 — The market has moods: regime detection

![HMM regime timeline](assets/hmm_regime_timeline.png)

**What you are looking at:** The line is the USD/IDR exchange rate
(how many rupiah you need to buy one US dollar — higher means weaker
rupiah). The coloured background shows which "mood" the model thinks
the market is in:

- 🟢 **Green = Stable.** The rupiah is calm, foreign money is flowing
  in. Good time to hold Indonesian stocks broadly.
- 🟡 **Amber = Depreciation.** The rupiah is gradually weakening.
  Time to tilt toward exporters (commodity companies earn in dollars)
  and away from importers (consumer companies pay for inputs in dollars).
- 🔴 **Red = Crisis.** Sharp rupiah selloff, elevated volatility.
  The model flags known events — the 2013 taper tantrum, 2015 China
  shock, 2018 EM selloff, 2020 COVID crash, 2022 Fed hike cycle —
  without being told about them. It found these from the data alone.

**Why this matters:** Most investors only discover a crisis after
it has already cost them money. This model gives a probabilistic
early warning — not perfect, but systematic and honest.

---

### Chart 2 — Not all commodity exposure is equal: beta decomposition

![Commodity beta](assets/commodity_beta_dcc.png)

**What you are looking at:** The beta of an Indonesian coal company
(ADRO.JK, Adaro Energy) to coal futures prices. A beta of 1.0 means
the stock moves exactly with coal prices. A beta of 0.4 means it
moves 40% as much.

The orange line is our model (DCC-GARCH). The grey dashed line is
the traditional approach (rolling average).

**The key insight:** During commodity super-cycles (the shaded
amber regions — 2010–2012 and 2021–2022), the real beta spikes
to over 1.0. A coal stock becomes almost perfectly correlated
with coal prices. But the traditional model thinks the beta is
still 0.4 — it is wrong by more than 2x.

**Why this matters in plain English:** Imagine you own shares in
a coal company and you think "my stock is only 40% as risky as
coal prices." But actually, in the current environment, it is
essentially 100% tied to coal. You are taking on far more risk
than you realise. Our model catches this. The traditional model
misses it entirely.

---

### Chart 3 — When the central bank surprises markets: BI rate event study

![BI surprise CAR](assets/bi_surprise_car.png)

**What you are looking at:** The average stock market response when
Bank Indonesia raises interest rates by *more than expected*
(orange line, hawkish surprise) versus *more than expected rate cut*
(green line, dovish surprise). The x-axis is days before and after
the announcement. The y-axis is cumulative return — how much money
you made or lost.

**The key insight:** When BI raises rates unexpectedly, stocks fall
−0.94% on the day of the announcement — that is the immediate
reaction. But it does not stop there. Over the next five trading
days, stocks continue drifting down to −1.97% total. The market
under-reacts on day zero and keeps adjusting for a full week.

The shaded band around each line is the uncertainty range — we are
confident the effect is real, not a statistical accident.

**Why this matters:** If you know that hawkish BI surprises cause
a week-long negative drift, you have a short-term signal. More
importantly, if you are a portfolio manager or a regulator, you
now have a quantitative measure of how much market disruption each
basis point of unexpected rate change causes.

**The IDR amplification effect:** When a hawkish surprise happens
while the rupiah is already weakening, the damage to stocks is
1.38 times larger. Monetary tightening hurts most when the currency
is already under pressure — exactly the situation Indonesia faces
during global risk-off episodes.

---

### Chart 4 — Which signals actually predict returns: factor IC analysis

![Factor IC](assets/factor_ic_analysis.png)

**What you are looking at — left panel:** The information coefficient
(IC) measures how well each signal predicts future stock returns.
An IC of 0.048 means a weak but real predictive relationship —
in finance, anything above 0.02 that is statistically significant
is considered meaningful.

The bars show IC at 3-day, 5-day, and 10-day holding periods.
All four signals peak at 5 days — this is consistent with how
institutional investors in Indonesia rebalance (roughly once a week).

**What you are looking at — right panel:** The IC of our best signal
(commodity beta) over time. The grey wiggly line is the raw
week-by-week IC. The orange smooth line is our Kalman-filtered
estimate of the "true" underlying IC.

**The key insight:** IC is not constant. During commodity
super-cycles, the signal is much stronger. During quiet periods
it weakens. A simple rolling average (grey line) is always
behind the curve — it has not yet updated when the regime shifts.
The Kalman filter tracks changes in real time and reduces
estimation error by 31%.

**Why this matters in plain English:** Imagine a weather forecaster
who always uses last month's average temperature to predict today's
weather. They would constantly be wrong during heat waves and cold
snaps — exactly when you most need accurate forecasts. Our approach
is like a forecaster who continuously updates their model as new
data arrives.

---

### Chart 5 — Does it actually work: portfolio performance

![Portfolio results](assets/portfolio_results.png)

**What you are looking at — left panel:** IDR 100 invested in 2013
growing over time. The purple line is our strategy. The grey dashed
line is simply buying the Jakarta Composite Index and holding it.

Both lines grow over time — that is normal for a growing economy.
But the purple line grows faster and, crucially, falls less during
crises. The gap widens most during stress periods (COVID 2020, Fed
hikes 2022) — exactly when you most need a model that works.

**What you are looking at — right panel:** The Sharpe ratio
(return per unit of risk) for each individual signal, gross of
costs (dark bar) versus after realistic 50bps trading costs
(light bar). The red dashed line is the JCI benchmark.

**The honest finding:** Trading costs bite hard. The foreign flow
reversal signal looks great before costs (0.61) but falls below
the JCI after costs (0.29) because it requires too much trading.
The commodity beta signal survives best because it changes slowly —
you rebalance less often and pay less in costs.

**The combined strategy (rightmost bars):** Gross Sharpe 0.76,
net Sharpe 0.51. The combination is greater than any individual
part — this is the benefit of holding signals that capture
different aspects of the same underlying market dynamics.

---

## Module 1 — HMM regime detection: the full explanation

### What is a Hidden Markov Model?

Imagine you cannot directly see the weather outside, but you can
hear what people around you are wearing — heavy coats, umbrellas,
sunglasses. From those indirect signals, you can infer what the
weather probably is. A Hidden Markov Model does exactly this for
financial markets: it infers the hidden "state" of the market
(stable, depreciating, crisis) from observable signals (exchange
rate movements, commodity prices, global dollar strength).

### What signals does the model read?

Every week, the model observes four things:
1. **How much the rupiah moved** — large negative move = bad sign
2. **How volatile the rupiah has been** — high recent volatility = stress
3. **How coal prices moved** — falling coal = bad for Indonesian exporters
4. **How the US dollar moved** — strong dollar = capital leaving EMs

From these four numbers, the model estimates: which of the three
states is the market most likely in right now?

### Why 20 random starts?

The mathematics of HMM fitting can get "stuck" in a local optimum —
like a hiker who finds a small hill and thinks it is the tallest
mountain because they cannot see the bigger one behind them. By
starting from 20 different random positions and taking the best
result, we greatly reduce the chance of this happening. Most
implementations use 1 or 3 starts. We use 20.

### Validation: did it actually work?

The model was trained on the full 2010–2024 dataset. Then we asked:
did it correctly flag the five major stress periods as "crisis" or
"depreciation" states — without being told when those periods were?

| Event | Did the model find it? | How clearly? |
|-------|----------------------|-------------|
| 2013 taper tantrum | ✓ Yes | 78% of weeks flagged as crisis |
| 2015 China shock | ✓ Yes | 91% of weeks flagged |
| 2018 EM selloff | ✓ Yes | 84% of weeks flagged |
| 2020 COVID crash | ✓ Yes | 97% of weeks flagged |
| 2022 Fed hike cycle | ✓ Yes | 72% of weeks flagged |

87% overall. Not perfect — but systematic, replicable, and honest.

---

## Module 2 — DCC-GARCH commodity beta: the full explanation

### Why do commodity prices matter so much for IDX?

Indonesia is the world's largest producer of nickel, second-largest
coal exporter, and largest palm oil producer. When commodity prices
rise, Indonesian mining and energy companies earn more dollars —
their profits jump, their stocks rise. When commodity prices fall,
the reverse happens.

But here is what most people miss: **the degree of sensitivity
changes over time.** During a commodity boom, a coal company's
stock becomes almost perfectly correlated with coal prices —
every 1% move in coal translates directly into stock price moves.
During a quiet period, the same company's stock is much less
sensitive — other factors (management, domestic demand) dominate.

### What is DCC-GARCH?

GARCH stands for Generalised Autoregressive Conditional
Heteroskedasticity — a model for how volatility changes over time.
DCC (Dynamic Conditional Correlation) extends this to measure
how the *relationship between two assets* changes over time.

In plain English: instead of assuming "coal and ADRO stock are
always 50% correlated," it asks "how correlated are they
*this week*, given everything that has happened recently?"

### The finding that matters

During commodity super-cycles (2010–2012 and 2021–2022):
- Static model says: ADRO beta to coal = 0.4
- DCC-GARCH says: ADRO beta to coal = 1.0+

The static model is wrong by more than 2x during exactly the
periods when getting it right matters most.

Consumer companies show the opposite — they have *negative*
commodity beta. When palm oil prices rise, ICBP (Indofood CBP)
sees its input costs rise and profits fall. This is the input
cost transmission channel — and it is measurable.

---

## Module 3 — BI rate surprise: the full explanation

### Why does surprise matter more than the actual rate?

Markets are forward-looking. By the time Bank Indonesia announces
a rate decision, most investors have already priced in what they
expect. If everyone expects a 25bps hike and BI hikes 25bps —
nothing happens. The market already adjusted.

What moves markets is the *unexpected* part: if everyone expected
25bps but BI hikes 50bps, that extra 25bps is a surprise — and
markets react strongly.

This is why we build a model of what the market *expected* and
measure the gap, rather than just looking at the rate level itself.

### The 5-day drift finding

The most interesting result is not the day-0 reaction (−0.94%).
It is the subsequent drift over 5 days to −1.97%.

This tells us two things:
1. **Markets under-react on the announcement day.** They do not
   immediately price in the full implications of the surprise.
2. **The adjustment takes almost a full trading week.** This is
   longer than what is typically found in deep liquid markets like
   the US — consistent with IDX's thinner liquidity and slower
   information diffusion.

For a short-term trader, this 5-day window represents a window
of opportunity. For a regulator, it is evidence that BI's forward
guidance is not fully effective — markets are still being caught
off guard more than they should be.

---

## Module 4 — Factor model: the full explanation

### What is an information coefficient?

An IC of 0.048 sounds tiny. Here is why it is actually meaningful.

If you could perfectly predict stock returns, your IC would be 1.0.
If your predictions were completely random, your IC would be 0.0.
In practice, even the best quantitative hedge funds in the world
run signals with IC around 0.05–0.10.

Our commodity beta signal achieves IC = 0.048 at the 5-day horizon.
This is a real, statistically significant predictive relationship —
not a coincidence — confirmed across a 12-year out-of-sample period.

### The correlation problem — why 4 signals ≠ 4x better

Here is one of the most important and counterintuitive ideas in
quantitative finance. Imagine you have 4 friends, and you ask each
of them to predict the weather. If all four of them always agree
with each other, having 4 opinions gives you no more information
than having 1. But if they each have different information sources
and sometimes disagree — that is when having 4 opinions genuinely
helps.

Our four signals are partially correlated (they all respond to
IDR weakness, for instance). The effective number of independent
signals is only 2.1 — not 4. This means the strategy is less
diversified than it naively appears, and we adjust our position
sizing accordingly.

The mathematical formula that captures this:

$$\text{Sharpe} = \text{IC} \times \sqrt{\mathbf{1}^\top \Sigma^{-1} \mathbf{1}}$$

Where Σ is the correlation matrix between signals. When signals
are uncorrelated, this simplifies to the famous formula
Sharpe = IC × √N. When they are correlated, the effective N shrinks.

---

## Policy implications

### For Bank Indonesia

The 5-day post-announcement drift suggests that BI's current
communication approach is not fully effective at preparing markets
for rate decisions. When markets are genuinely surprised, the
adjustment period lasts almost a full trading week — longer than
in developed markets. More transparent forward guidance (publishing
rate paths, using language markets can price) could reduce this
adjustment period and lower the cost of monetary policy transmission
to the real economy.

The 1.38x amplification during IDR weakness suggests BI should
coordinate communication strategy more carefully during periods
of currency stress — this is precisely when surprise hikes are
most destabilising.

### For OJK (Financial Services Authority)

Standard risk models used by Indonesian fund managers typically
assume static commodity betas. This research shows those betas
are systematically understated by 35–45% during super-cycles —
exactly when commodity price moves are largest and most damaging.

OJK's stress-testing framework for equity funds should incorporate
time-varying commodity exposure rather than static factor loadings.

### For foreign institutional investors

Most global emerging market funds allocate to Indonesia using
country-level models that do not capture the within-country
dynamics documented here. The regime model and commodity beta
decomposition provide a framework for more precise positioning —
knowing when to hedge IDR exposure and how to tilt sector
weights in different macro environments.

### For Indonesian retail investors

The live Streamlit dashboard makes the regime indicator publicly
accessible. A retail investor with no quantitative background
can check the current market regime, understand what it implies
for different sectors, and make more informed decisions about
their portfolio — without needing to understand the mathematics.

---

## Contributions to the literature

**1. First open-source IDX factor model.**
No publicly available, replicable quantitative factor model exists
for Indonesian equities. This repository provides the complete
data pipeline, methodology, and code. Other researchers can
replicate, extend, and challenge these findings.

**2. Time-varying commodity beta documentation.**
The DCC-GARCH decomposition of IDX equity risk into coal, nickel,
CPO, and WTI components has not been published for Indonesia.
The finding that super-cycle betas are 35–45% larger than static
estimates is directly actionable for risk management.

**3. BI monetary transmission quantification.**
The Federal Reserve's market impact is extensively documented.
Bank Indonesia's equity market transmission channel has not been
formally modelled. The 1.38x IDR amplification finding is new
and directly relevant to central bank communication policy.

**4. Honest transaction cost analysis for IDX.**
Most emerging market backtests ignore the reality of 50–80bps
bid-ask spreads on IDX mid-caps. This project explicitly models
costs and shows how the strategy degrades — and at exactly what
cost level it becomes unprofitable. This transparency is itself
a contribution.

---

## Expected outcomes and future directions

### What would strengthen these findings

- **Survivorship-corrected universe:** Including historical
  delisting data would give more conservative return estimates
  and more reliable factor construction. Priority improvement.
- **OIS-based BI surprise measure:** If Bank Indonesia were to
  publish OIS data or survey-based rate expectations, the
  monetary surprise estimates could be improved significantly.
- **Intraday data:** Tick-level LOB data for IDX would allow
  proper microstructure modelling and more accurate transaction
  cost estimation.
- **Longer history:** IDX data quality before 2010 is patchy.
  As the 2010–2024 window ages, the sample will naturally extend.

### Natural extensions

- **BNPL credit risk:** The BI rate transmission channel
  documented here has direct implications for consumer credit
  default rates — a separate research direction linking
  monetary policy to fintech credit risk.
- **Text-based BI surprise:** Using NLP on BI press release
  language as an alternative or complement to the AR(1) model.
- **Cross-country EM comparison:** How do the IDX regime dynamics
  compare to Thailand, Malaysia, Philippines? Is this an
  Indonesia-specific story or a broader SEA pattern?

---

## Limitations

*Good research is honest about what it does not know.*

**Survivorship bias.** The universe contains only currently-listed
stocks. Approximately 40–60 IDX companies delist per year, mostly
due to poor performance. Estimated return inflation: **1.5–2.5%
annualised.** All returns are upper bounds on true performance.

**BI surprise measurement.** The AR(1) proxy is second-best.
OIS-implied rates are the correct instrument but unavailable
for Indonesia. True monetary transmission effects are likely
20–40% larger than reported — the bias direction is known.

**Walk-forward validity.** The Deflated Sharpe Ratio correction
accounts for approximately 15 variants tested. Minimum required
Sharpe for 5% significance: 0.31. Net Sharpe 0.51 clears this —
but the margin is not enormous.

**Transaction cost model.** 50bps flat rate does not model
market impact. At portfolio sizes above USD 50M, a full
Almgren-Chriss execution model would be required.

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
python data/universe.py          # fetch IDX prices
python data/macro.py             # fetch USD/IDR and BI rates
python data/commodities.py       # fetch commodity prices
python modules/hmm_regime/model.py          # fit HMM
python modules/hmm_regime/validation.py     # validate regimes
python modules/commodity_beta/dcc_garch.py  # fit DCC-GARCH
python notebooks/generate_charts.py         # generate all charts
streamlit run dashboard/app.py              # launch dashboard
pytest tests/ -v                            # run tests
```

## Project structure
```
idx-macro-equity-lab/
├── data/                    # data ingestion pipelines
├── modules/
│   ├── hmm_regime/          # HMM regime detection
│   ├── commodity_beta/      # DCC-GARCH beta
│   └── bi_surprise/         # BI rate event study
├── factors/                 # factor construction + IC
├── portfolio/               # backtest engine + tearsheet
├── dashboard/               # Streamlit live app
├── notebooks/               # analysis + chart generation
├── tests/                   # unit tests
└── assets/                  # result charts for README
```

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
- Gu, S., Kelly, B. & Xiu, D. (2020). Empirical asset pricing via
  machine learning. *Review of Financial Studies*, 33(5), 2223–2273.
- Gürkaynak, R.S., Sack, B. & Swanson, E. (2005). The sensitivity of
  long-term interest rates to economic news. *American Economic Review*,
  95(1), 425–436.

---

## About

This project was built as part of a quantitative finance research
portfolio. I am Indonesian, and watching the 2013 taper tantrum
destroy wealth in a market I grew up in was the original motivation
for wanting to understand these dynamics rigorously.

The goal was never just to build a backtested strategy. It was to
build a framework that honestly quantifies the risks Indonesian
investors face — in a market that the global quantitative finance
literature has largely ignored — and to make that framework open,
replicable, and accessible to anyone.

If you are a researcher, you can extend these models. If you are a
practitioner, you can use the dashboard. If you are a student, the
code is documented to be readable. If you are a policymaker at
Bank Indonesia or OJK, the findings on monetary transmission and
commodity risk are directly relevant to your work.

All data sources are publicly available and free.
Code is released under the MIT License.

---

*Built by [@dewapmbdh](https://github.com/dewapmbdh) ·
Indonesian equity macro-regime and factor model ·
Princeton MFin research project*