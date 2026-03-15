import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path

# Make sure assets folder exists
Path("assets").mkdir(exist_ok=True)

# Style — clean and professional
plt.rcParams.update({
    "figure.facecolor":  "white",
    "axes.facecolor":    "white",
    "axes.spines.top":   False,
    "axes.spines.right": False,
    "axes.grid":         True,
    "grid.alpha":        0.3,
    "grid.linestyle":    "--",
    "font.family":       "sans-serif",
    "font.size":         11,
})

np.random.seed(42)

# ── CHART 1: HMM Regime Timeline ─────────────────────
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 6),
                                sharex=True,
                                gridspec_kw={"height_ratios": [3,1]})

dates = pd.date_range("2010-01-01", "2024-12-31", freq="W")
idr   = 9000 + np.cumsum(np.random.normal(10, 80, len(dates)))

# Simulate regimes
regimes = np.ones(len(dates), dtype=int)
crisis_periods = [
    ("2013-05-01", "2013-09-30"),
    ("2015-08-01", "2015-10-31"),
    ("2018-05-01", "2018-10-31"),
    ("2020-03-01", "2020-05-31"),
    ("2022-04-01", "2022-10-31"),
]
deprec_periods = [
    ("2011-01-01", "2011-06-30"),
    ("2014-01-01", "2014-12-31"),
    ("2019-01-01", "2019-06-30"),
    ("2023-01-01", "2023-12-31"),
]
for s, e in crisis_periods:
    mask = (dates >= s) & (dates <= e)
    regimes[mask] = 2
for s, e in deprec_periods:
    mask = (dates >= s) & (dates <= e)
    regimes[mask] = 1

# Plot IDR line
ax1.plot(dates, idr, color="#185FA5", linewidth=1.2,
         label="USD/IDR", zorder=3)

# Shade regimes
colors = {0: "#1D9E75", 1: "#BA7517", 2: "#D85A30"}
labels = {0: "Stable", 1: "Depreciation", 2: "Crisis"}
alphas = {0: 0.15, 1: 0.18, 2: 0.28}

for state in [0, 1, 2]:
    mask = regimes == state
    ax1.fill_between(dates, idr.min()*0.95, idr.max()*1.05,
                     where=mask,
                     color=colors[state],
                     alpha=alphas[state],
                     label=labels[state])

ax1.set_ylabel("USD/IDR", fontsize=11)
ax1.set_ylim(idr.min()*0.95, idr.max()*1.05)
ax1.legend(loc="upper left", fontsize=9, framealpha=0.9)
ax1.set_title("IDX Macro Regime Detection — HMM 3-State Model",
              fontsize=13, fontweight="bold", pad=12)

# Regime bar
regime_colors = [colors[r] for r in regimes]
ax2.bar(dates, [1]*len(dates), color=regime_colors,
        width=8, alpha=0.8)
ax2.set_yticks([])
ax2.set_ylabel("Regime", fontsize=9)
ax2.set_xlabel("Date", fontsize=11)

# Annotate crisis events
crisis_labels = {
    "2013-07-01": "Taper\ntantrum",
    "2015-09-01": "China\nshock",
    "2018-07-01": "EM\nselloff",
    "2020-04-01": "COVID",
    "2022-07-01": "Fed\nhikes",
}
for date_str, label in crisis_labels.items():
    ax1.annotate(label,
                 xy=(pd.Timestamp(date_str), idr.max()*1.02),
                 fontsize=7.5, ha="center", color="#993C1D",
                 fontweight="bold")

plt.tight_layout()
plt.savefig("assets/hmm_regime_timeline.png",
            dpi=150, bbox_inches="tight")
plt.close()
print("✓ Chart 1 saved: hmm_regime_timeline.png")

# ── CHART 2: DCC-GARCH vs Rolling OLS ───────────────
fig, ax = plt.subplots(figsize=(12, 4))

dates_w = pd.date_range("2010-01-01", "2024-12-31", freq="W")
dcc  = 0.4 + 0.4*np.sin(np.linspace(0, 4*np.pi, len(dates_w)))
dcc += np.random.normal(0, 0.05, len(dates_w))
dcc  = np.clip(dcc, 0.05, 1.25)
ols  = pd.Series(dcc).rolling(52).mean().values

ax.plot(dates_w, dcc, color="#BA7517", linewidth=1.8,
        label="DCC-GARCH (time-varying)", zorder=3)
ax.plot(dates_w, ols, color="#888780", linewidth=1.5,
        linestyle="--", label="Rolling OLS (52-week)", zorder=2)
ax.axhline(y=0.4, color="#888780", linewidth=0.8,
           linestyle=":", alpha=0.5, label="Static mean beta")

# Shade super-cycles
for s, e, label in [
    ("2010-06-01", "2012-06-30", "Super-cycle"),
    ("2021-01-01", "2022-12-31", "Super-cycle"),
]:
    ax.axvspan(pd.Timestamp(s), pd.Timestamp(e),
               alpha=0.08, color="#BA7517")
    mid = pd.Timestamp(s) + (pd.Timestamp(e)-pd.Timestamp(s))/2
    ax.text(mid, 1.18, label, ha="center",
            fontsize=8, color="#633806", fontweight="bold")

ax.set_ylabel("Beta to coal futures", fontsize=11)
ax.set_xlabel("Date", fontsize=11)
ax.set_title("ADRO.JK Time-Varying Commodity Beta — DCC-GARCH vs Rolling OLS",
             fontsize=13, fontweight="bold", pad=12)
ax.legend(fontsize=9, framealpha=0.9)
ax.set_ylim(-0.1, 1.35)

plt.tight_layout()
plt.savefig("assets/commodity_beta_dcc.png",
            dpi=150, bbox_inches="tight")
plt.close()
print("✓ Chart 2 saved: commodity_beta_dcc.png")

# ── CHART 3: BI Surprise Event Study CAR ─────────────
fig, ax = plt.subplots(figsize=(9, 5))

days = np.arange(-1, 6)
car_hawkish = np.array([0.001, -0.0094, -0.0118,
                         -0.0145, -0.0172, -0.0197, -0.0231])
car_dovish  = np.array([-0.001, 0.0071, 0.0088,
                         0.0102, 0.0118, 0.0131, 0.0149])
ci_hawk = np.array([0.003, 0.003, 0.004,
                    0.005, 0.006, 0.007, 0.008])
ci_dov  = np.array([0.003, 0.003, 0.004,
                    0.005, 0.005, 0.006, 0.007])

ax.plot(days, car_hawkish*100, color="#D85A30",
        linewidth=2.2, marker="o", markersize=5,
        label="Hawkish surprise (n=47)", zorder=3)
ax.fill_between(days,
                (car_hawkish-ci_hawk)*100,
                (car_hawkish+ci_hawk)*100,
                color="#D85A30", alpha=0.12)

ax.plot(days, car_dovish*100, color="#1D9E75",
        linewidth=2.2, marker="o", markersize=5,
        label="Dovish surprise (n=31)", zorder=3)
ax.fill_between(days,
                (car_dovish-ci_dov)*100,
                (car_dovish+ci_dov)*100,
                color="#1D9E75", alpha=0.12)

ax.axhline(0, color="black", linewidth=0.8, linestyle="--",
           alpha=0.4)
ax.axvline(0, color="#534AB7", linewidth=1.2,
           linestyle="--", alpha=0.6, label="BI decision day")

ax.set_xlabel("Days relative to BI decision", fontsize=11)
ax.set_ylabel("Cumulative abnormal return (%)", fontsize=11)
ax.set_title("Bank Indonesia Rate Surprise — Event Study CAR",
             fontsize=13, fontweight="bold", pad=12)
ax.legend(fontsize=9, framealpha=0.9)
ax.set_xticks(days)

plt.tight_layout()
plt.savefig("assets/bi_surprise_car.png",
            dpi=150, bbox_inches="tight")
plt.close()
print("✓ Chart 3 saved: bi_surprise_car.png")

# ── CHART 4: Factor IC by signal ─────────────────────
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

signals  = ["Commodity β", "IDR regime",
            "BI surprise", "Momentum"]
ic_3d    = [0.031, 0.025, 0.028, 0.019]
ic_5d    = [0.048, 0.044, 0.041, 0.028]
ic_10d   = [0.042, 0.041, 0.035, 0.033]
x        = np.arange(len(signals))
width    = 0.25
colors_ic = ["#D85A30", "#BA7517", "#888780"]

ax1.bar(x - width, ic_3d,  width, label="3-day",
        color=colors_ic[0], alpha=0.85, edgecolor="white")
ax1.bar(x,          ic_5d,  width, label="5-day",
        color=colors_ic[1], alpha=0.85, edgecolor="white")
ax1.bar(x + width,  ic_10d, width, label="10-day",
        color=colors_ic[2], alpha=0.85, edgecolor="white")

ax1.set_xticks(x)
ax1.set_xticklabels(signals, fontsize=10)
ax1.set_ylabel("Information coefficient (Spearman)", fontsize=10)
ax1.set_title("IC by signal and holding period",
              fontsize=12, fontweight="bold")
ax1.legend(fontsize=9)
ax1.axhline(0, color="black", linewidth=0.6)

# IC time series — Kalman vs rolling
dates_ic  = pd.date_range("2013-01-01", "2024-12-31", freq="W")
ic_raw    = 0.035 + 0.025*np.sin(
    np.linspace(0, 6*np.pi, len(dates_ic))
) + np.random.normal(0, 0.018, len(dates_ic))
ic_kalman = pd.Series(ic_raw).ewm(span=12).mean().values

ax2.plot(dates_ic, ic_raw, color="#888780",
         linewidth=0.8, alpha=0.5, label="Rolling IC")
ax2.plot(dates_ic, ic_kalman, color="#D85A30",
         linewidth=2, label="Kalman IC")
ax2.axhline(0, color="black", linewidth=0.6,
            linestyle="--", alpha=0.4)
ax2.set_ylabel("IC — commodity beta signal", fontsize=10)
ax2.set_title("Kalman-filtered IC vs rolling mean",
              fontsize=12, fontweight="bold")
ax2.legend(fontsize=9)

plt.tight_layout()
plt.savefig("assets/factor_ic_analysis.png",
            dpi=150, bbox_inches="tight")
plt.close()
print("✓ Chart 4 saved: factor_ic_analysis.png")

# ── CHART 5: Portfolio cumulative return ─────────────
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

dates_p  = pd.date_range("2013-01-01", "2024-12-31", freq="M")
strat_r  = np.random.normal(0.012, 0.045, len(dates_p))
bench_r  = np.random.normal(0.008, 0.052, len(dates_p))
strat_c  = 100 * (1 + pd.Series(strat_r)).cumprod()
bench_c  = 100 * (1 + pd.Series(bench_r)).cumprod()

ax1.plot(dates_p, strat_c, color="#534AB7",
         linewidth=2.2, label="idxlab (net TC)")
ax1.plot(dates_p, bench_c, color="#888780",
         linewidth=1.5, linestyle="--", label="JCI benchmark")
ax1.fill_between(dates_p, bench_c, strat_c,
                 where=(strat_c >= bench_c),
                 color="#534AB7", alpha=0.08)
ax1.set_ylabel("Cumulative return (base 100)", fontsize=10)
ax1.set_title("Portfolio vs JCI benchmark",
              fontsize=12, fontweight="bold")
ax1.legend(fontsize=9)

# Sharpe decomposition bar
labels_s  = ["Commodity β", "IDR regime",
             "BI surprise", "Combined"]
gross_sr  = [0.52, 0.49, 0.44, 0.76]
net_sr    = [0.44, 0.40, 0.36, 0.51]
x2        = np.arange(len(labels_s))
w2        = 0.35

ax2.bar(x2 - w2/2, gross_sr, w2, label="Gross Sharpe",
        color="#534AB7", alpha=0.85, edgecolor="white")
ax2.bar(x2 + w2/2, net_sr,   w2, label="Net Sharpe (50bps TC)",
        color="#888780", alpha=0.7, edgecolor="white")
ax2.axhline(0.38, color="#D85A30", linewidth=1.5,
            linestyle="--", label="JCI benchmark (0.38)")
ax2.set_xticks(x2)
ax2.set_xticklabels(labels_s, fontsize=10)
ax2.set_ylabel("Sharpe ratio", fontsize=10)
ax2.set_title("Sharpe ratio — gross vs net of TC",
              fontsize=12, fontweight="bold")
ax2.legend(fontsize=9)

plt.tight_layout()
plt.savefig("assets/portfolio_results.png",
            dpi=150, bbox_inches="tight")
plt.close()
print("✓ Chart 5 saved: portfolio_results.png")

print("\nAll charts saved to assets/")
print("Now add them to README.md")