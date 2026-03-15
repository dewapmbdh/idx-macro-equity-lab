import numpy as np
import pandas as pd

KNOWN_CRISES = {
    "taper_tantrum":  ("2013-05-01", "2013-09-30"),
    "china_shock":    ("2015-08-01", "2015-10-31"),
    "em_selloff":     ("2018-05-01", "2018-10-31"),
    "covid_crash":    ("2020-03-01", "2020-05-31"),
    "fed_hike_2022":  ("2022-04-01", "2022-10-31"),
}

def validate(states, dates):
    state_series = pd.Series(states, index=dates)
    crisis_state = pd.Series(states).value_counts().idxmin()
    results = {}
    for name, (start, end) in KNOWN_CRISES.items():
        mask = (dates >= start) & (dates <= end)
        if mask.sum() == 0:
            continue
        pct = (state_series[mask] == crisis_state).mean()
        results[name] = round(pct, 2)
        detected = "YES" if pct > 0.5 else "NO"
        print(f"  {name}: {pct:.0%} crisis state → {detected}")
    overall = np.mean([v > 0.5 for v in results.values()])
    print(f"\n  Overall detection rate: {overall:.0%}")
    return results

if __name__ == "__main__":
    from data.macro import fetch_usdidr
    from data.commodities import fetch_commodities
    from modules.hmm_regime.model import fit_regime_model
    idr   = fetch_usdidr()
    comms = fetch_commodities()
    model, states, probs, dates = fit_regime_model(idr, comms)
    print("\nValidating against known crisis periods:")
    validate(states, dates)