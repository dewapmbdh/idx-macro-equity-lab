import pandas as pd
import numpy as np

def compute_tearsheet(returns, benchmark=None):
    ann = 52
    ar  = (1+returns).prod()**(ann/len(returns)) - 1
    vol = returns.std() * np.sqrt(ann)
    cum = (1+returns).cumprod()
    mdd = (cum/cum.cummax()-1).min()

    if benchmark is not None:
        exc = returns - benchmark.reindex(
            returns.index).fillna(0)
        sr = exc.mean() / exc.std() * np.sqrt(ann)
    else:
        sr = (returns.mean() / returns.std()) * np.sqrt(ann)

    metrics = {
        "annualised_return": round(ar, 4),
        "annualised_vol":    round(vol, 4),
        "sharpe_ratio":      round(sr, 3),
        "max_drawdown":      round(mdd, 4),
        "hit_rate":          round((returns>0).mean(), 3),
        "calmar":            round(ar/abs(mdd), 3),
    }

    print("\nPortfolio Tearsheet")
    print("="*35)
    for k, v in metrics.items():
        print(f"  {k:<22} {v}")
    return metrics

if __name__ == "__main__":
    print("Tearsheet module ready")