import numpy as np
import pandas as pd
from scipy import stats

def compute_surprise(bi_decisions):
    rates = bi_decisions["rate_pct"].dropna()
    expected = rates.shift(1) * 0.9 + rates.mean() * 0.1
    surprise = (rates - expected) * 100
    return surprise.rename("bi_surprise_bps")

def event_study(returns, event_dates, surprise,
                window=(-1, 5)):
    mkt = returns.mean(axis=1)
    results = []

    for date in event_dates:
        if date not in returns.index:
            continue
        idx = returns.index.get_loc(date)
        w_start = max(0, idx + window[0])
        w_end   = min(len(returns)-1, idx + window[1])

        r_event = returns.iloc[w_start:w_end+1]
        m_event = mkt.iloc[w_start:w_end+1]
        ar  = r_event.subtract(m_event, axis=0)
        car = ar.mean(axis=1).sum()

        surp = surprise.get(date, np.nan)
        results.append({
            "date":         date,
            "car":          car,
            "surprise_bps": surp,
            "direction":    "hawkish" if surp > 0
                            else "dovish" if surp < 0
                            else "neutral"
        })

    df = pd.DataFrame(results).set_index("date")
    print("\nBI Surprise Event Study Results:")
    print(f"Total events: {len(df)}")
    print(f"Hawkish: {(df.direction=='hawkish').sum()}")
    print(f"Dovish:  {(df.direction=='dovish').sum()}")
    print(f"\nAvg CAR hawkish: {df[df.direction=='hawkish'].car.mean():.4f}")
    print(f"Avg CAR dovish:  {df[df.direction=='dovish'].car.mean():.4f}")
    return df

if __name__ == "__main__":
    print("BI surprise module ready")
    print("Needs data/raw/bi_decisions.csv to run full analysis")