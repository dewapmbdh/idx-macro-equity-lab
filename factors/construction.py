import pandas as pd
import numpy as np

def build_factors(returns, market_caps):
    cap = market_caps.reindex(returns.columns).fillna(0)
    cap_threshold = cap.quantile(0.20)
    liquid = cap[cap > cap_threshold].index
    ret = returns[liquid]
    cap = cap[liquid]

    # MKT — value weighted excess return
    weights  = cap / cap.sum()
    mkt_ret  = (ret * weights).sum(axis=1)
    rf_weekly = (1 + 0.055) ** (1/52) - 1
    mkt = mkt_ret - rf_weekly

    # SMB — small minus big
    size_median = cap.median()
    small = cap[cap <= size_median].index
    big   = cap[cap >  size_median].index
    smb   = ret[small].mean(axis=1) - ret[big].mean(axis=1)

    # UMD — momentum 12-1 month
    cum_ret  = (1 + ret).rolling(52).apply(np.prod, raw=True) - 1
    mom      = cum_ret.shift(4)
    mom_rank = mom.rank(axis=1, pct=True)

    factors = pd.DataFrame({
        "MKT": mkt,
        "SMB": smb,
    }).dropna()

    return factors

if __name__ == "__main__":
    print("Factor construction module ready")