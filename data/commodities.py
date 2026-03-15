import yfinance as yf
import pandas as pd

COMMODITY_TICKERS = {
    "coal":   "MTF=F",
    "nickel": "NI=F",
    "wti":    "CL=F",
    "gold":   "GC=F",
    "dxy":    "DX-Y.NYB",
}

def fetch_commodities(start="2010-01-01"):
    dfs = {}
    for name, ticker in COMMODITY_TICKERS.items():
        try:
            s = yf.download(
                ticker, start=start,
                auto_adjust=True, progress=False
            )["Close"]
            dfs[name] = s
        except Exception as e:
            print(f"Failed {name}: {e}")
    df = pd.DataFrame(dfs).ffill(limit=2)
    return df.pct_change().dropna(how="all")

if __name__ == "__main__":
    comms = fetch_commodities()
    print(comms.tail(3))