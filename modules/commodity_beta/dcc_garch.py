import numpy as np
import pandas as pd
from arch import arch_model
from scipy.optimize import minimize

def fit_univariate_garch(returns):
    model = arch_model(
        returns * 100,
        vol="Garch", p=1, o=1, q=1,
        dist="skewt", rescale=False
    )
    result = model.fit(disp="off", show_warning=False)
    std_resid = result.resid / result.conditional_volatility
    cond_vol  = result.conditional_volatility / 100
    return std_resid, cond_vol

def fit_dcc(std_resids):
    E    = std_resids.values
    T, N = E.shape
    Qbar = np.cov(E.T)

    def neg_ll(params):
        a, b = params
        if a <= 0 or b <= 0 or a + b >= 1:
            return 1e10
        Q, ll = Qbar.copy(), 0.0
        for t in range(1, T):
            e = E[t-1:t].T
            Q = (1-a-b)*Qbar + a*(e@e.T) + b*Q
            d = np.sqrt(np.diag(Q))
            R = Q / np.outer(d, d)
            np.fill_diagonal(R, 1.0)
            try:
                s, ld = np.linalg.slogdet(R)
                if s <= 0: return 1e10
                et = E[t:t+1].T
                ll += -0.5*(ld + float(
                    et.T @ np.linalg.solve(R, et)))
            except Exception:
                return 1e10
        return -ll

    res = minimize(
        neg_ll, [0.02, 0.95],
        bounds=[(1e-4, 0.2), (0.7, 0.999)],
        method="L-BFGS-B"
    )
    a, b = res.x
    Q, corrs = Qbar.copy(), []
    for t in range(T):
        if t > 0:
            e = E[t-1:t].T
            Q = (1-a-b)*Qbar + a*(e@e.T) + b*Q
        d = np.sqrt(np.diag(Q))
        R = Q / np.outer(d, d)
        np.fill_diagonal(R, 1.0)
        corrs.append(R.copy())
    return {
        "a": a, "b": b,
        "correlations": np.array(corrs),
        "converged": res.success
    }

if __name__ == "__main__":
    from data.universe import fetch_prices
    from data.commodities import fetch_commodities
    print("Fetching data...")
    _, returns = fetch_prices()
    comms = fetch_commodities()
    
    # Test on one stock vs coal
    stock = returns["ADRO.JK"].dropna()
    coal  = comms["coal"].dropna()
    combined = pd.concat([stock, coal], axis=1).dropna()
    combined.columns = ["ADRO", "coal"]
    combined = combined.resample("W-FRI").last().dropna()

    print("Fitting GARCH models...")
    std_resids = pd.DataFrame()
    for col in combined.columns:
        sr, _ = fit_univariate_garch(combined[col])
        std_resids[col] = sr.values[:len(combined)]

    print("Fitting DCC...")
    result = fit_dcc(std_resids.dropna())
    print(f"DCC converged: {result['converged']}")
    print(f"a={result['a']:.4f}, b={result['b']:.4f}")
    print(f"Correlation shape: {result['correlations'].shape}")