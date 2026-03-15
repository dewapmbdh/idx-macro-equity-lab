import yfinance as yf
import pandas as pd
import numpy as np

IDX_UNIVERSE = {
    "BBCA.JK": "Financials", "BBRI.JK": "Financials",
    "BMRI.JK": "Financials", "BBNI.JK": "Financials",
    "TLKM.JK": "Telecom",   "ASII.JK": "Consumer",
    "ICBP.JK": "Consumer",  "UNVR.JK": "Consumer",
    "BYAN.JK": "Energy",    "ADRO.JK": "Energy",
    "PTBA.JK": "Energy",    "ITMG.JK": "Energy",
    "INCO.JK": "Materials", "ANTM.JK": "Materials",
    "GOTO.JK": "Tech",      "BUKA.JK": "Tech",
    "JSMR.JK": "Infra",     "BSDE.JK": "Property",
    "AALI.JK": "Agri",      "LSIP.JK": "Agri",
}

def fetch_prices(start="2010-01-01"):
    tickers = list(IDX_UNIVERSE.keys())
    raw = yf.download(
        tickers, start=start,
        auto_adjust=True, progress=False
    )
    close = raw["Close"].copy()
    close = close.where(close > 0)
    close = close.ffill(limit=5)
    returns = close.pct_change()
    returns = returns.clip(
        lower=returns.quantile(0.01),
        upper=returns.quantile(0.99),
        axis=1
    )
    return close, returns

if __name__ == "__main__":
    print("Downloading IDX prices...")
    prices, returns = fetch_prices()
    print(f"Stocks: {prices.shape[1]}")
    print(f"From: {prices.index[0].date()}")
    print(f"To:   {prices.index[-1].date()}")
    print(returns.tail(3))