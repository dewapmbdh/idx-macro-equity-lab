import pandas as pd
import numpy as np
from scipy import stats

def rolling_ic(signal, forward_returns,
               horizon=5, window=52):
    fwd = forward_returns.shift(-horizon)
    ic_list = []

    for i, date in enumerate(signal.index[window:], window):
        w_dates = signal.index[i-window:i]
        s = signal.loc[w_dates].stack().dropna()
        r = fwd.loc[w_dates].stack().dropna()
        common = s.index.intersection(r.index)
        if len(common) < 30:
            ic_list.append((date, np.nan))
            continue
        ic, _ = stats.spearmanr(s[common], r[common])
        ic_list.append((date, ic))

    return pd.Series(dict(ic_list), name=f"IC_{horizon}d")

def kalman_ic(raw_ic):
    ic = raw_ic.dropna().values
    R  = np.var(ic)
    Q  = np.var(np.diff(ic))
    x, P = ic[0], R
    filtered = [x]
    for t in range(1, len(ic)):
        P = P + Q
        K = P / (P + R)
        x = x + K * (ic[t] - x)
        P = (1 - K) * P
        filtered.append(x)
    return pd.Series(
        filtered,
        index=raw_ic.dropna().index,
        name="IC_kalman"
    )

def ic_summary(ic_series):
    clean = ic_series.dropna()
    print(f"\nIC Summary — {ic_series.name}")
    print(f"  Mean IC:    {clean.mean():.4f}")
    print(f"  Std IC:     {clean.std():.4f}")
    print(f"  ICIR:       {clean.mean()/clean.std():.3f}")
    print(f"  % positive: {(clean>0).mean():.1%}")
    return {
        "mean_ic": round(clean.mean(), 4),
        "icir":    round(clean.mean()/clean.std(), 3),
        "pct_pos": round((clean>0).mean(), 3),
    }

if __name__ == "__main__":
    print("IC analysis module ready")