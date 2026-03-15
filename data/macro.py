import pandas as pd
import pandas_datareader as pdr

def fetch_usdidr(start="2010-01-01"):
    df = pdr.get_data_fred("DEXINUS", start=start)
    return df["DEXINUS"].rename("USDIDR").ffill()

if __name__ == "__main__":
    idr = fetch_usdidr()
    print(f"USD/IDR latest: {idr.iloc[-1]:.0f}")
    print(f"Date range: {idr.index[0].date()} to {idr.index[-1].date()}")