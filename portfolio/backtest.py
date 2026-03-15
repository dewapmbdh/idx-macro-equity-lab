import pandas as pd
import numpy as np

def walk_forward_backtest(signals, returns,
                          rebal_freq="M", tc=0.005):
    rebal_dates = pd.date_range(
        returns.index[0], returns.index[-1],
        freq=rebal_freq
    )
    port_returns = []
    prev_weights = pd.Series(dtype=float)

    for i, d in enumerate(rebal_dates[:-1]):
        next_d = rebal_dates[i+1]
        sig = signals.loc[:d].iloc[-1].dropna()
        if len(sig) < 10:
            continue

        ranks = sig.rank(pct=True)
        longs = ranks[ranks >= 0.80].index
        if len(longs) == 0:
            continue

        w = pd.Series(1.0/len(longs), index=longs)
        w = w.clip(upper=0.05)
        w = w / w.sum()

        # Transaction costs
        all_s   = w.index.union(prev_weights.index)
        w_full  = w.reindex(all_s, fill_value=0)
        pw_full = prev_weights.reindex(all_s, fill_value=0)
        to      = (w_full - pw_full).abs().sum() / 2
        tc_drag = to * tc

        pr = returns.loc[d:next_d, w.index].iloc[1:]
        if pr.empty:
            continue

        r = (pr * w).sum(axis=1)
        r.iloc[0] -= tc_drag
        port_returns.append(r)
        prev_weights = w

    if not port_returns:
        return pd.Series(dtype=float)
    return pd.concat(port_returns)

if __name__ == "__main__":
    print("Backtest engine ready")