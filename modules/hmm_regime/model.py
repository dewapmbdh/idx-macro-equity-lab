import numpy as np
import pandas as pd
from hmmlearn import hmm
from sklearn.preprocessing import StandardScaler

def fit_regime_model(usdidr, commodity_returns, n_states=3):
    weekly_idr = usdidr.resample("W-FRI").last()
    idr_ret = np.log(weekly_idr).diff()
    idr_vol = idr_ret.rolling(4).std()

    features = pd.DataFrame({
        "idr_return": idr_ret,
        "idr_vol":    idr_vol,
        "coal_ret":   commodity_returns.get(
                        "coal", pd.Series(dtype=float)),
        "dxy_ret":    commodity_returns.get(
                        "dxy", pd.Series(dtype=float)),
    }).dropna()

    scaler = StandardScaler()
    obs = scaler.fit_transform(features.values)

    best_ll, best_model = -np.inf, None
    for seed in range(20):
        model = hmm.GaussianHMM(
            n_components=n_states,
            covariance_type="full",
            n_iter=500,
            random_state=seed
        )
        try:
            model.fit(obs)
            ll = model.score(obs)
            if ll > best_ll:
                best_ll, best_model = ll, model
        except Exception:
            continue

    states = best_model.predict(obs)
    probs = pd.DataFrame(
        best_model.predict_proba(obs),
        index=features.index,
        columns=[f"state_{i}" for i in range(n_states)]
    )
    return best_model, states, probs, features.index

if __name__ == "__main__":
    from data.macro import fetch_usdidr
    from data.commodities import fetch_commodities
    print("Fetching data...")
    idr   = fetch_usdidr()
    comms = fetch_commodities()
    print("Fitting HMM...")
    model, states, probs, dates = fit_regime_model(idr, comms)
    print(f"States found: {np.unique(states)}")
    print(f"State counts: {pd.Series(states).value_counts().to_dict()}")
    print(probs.tail(5))