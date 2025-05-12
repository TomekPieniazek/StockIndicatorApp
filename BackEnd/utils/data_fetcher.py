import yfinance as yf
import pandas as pd

class DataFetcher:
    @staticmethod
    def get_data(tickers, period="1y", interval="1d") -> pd.DataFrame:
        df_dict = {}
        for t in tickers:
            try:
                tmp = yf.download(t, period=period, interval=interval, progress=False)["Close"]
                if tmp.empty:
                    print(f"[DataFetcher] no data for {t}, skipping.")
                    continue
                if isinstance(tmp, pd.Series):
                    df_dict[t] = tmp
                else:
                    df_dict[t] = tmp[t]
            except Exception as e:
                print(f"[DataFetcher] failed to fetch {t}: {e}")
        if not df_dict:
            raise ValueError("[DataFetcher] none of the tickers returned data!")
        df = pd.DataFrame(df_dict).dropna()
        if df.empty:
            raise ValueError("[DataFetcher] dropna() removed all rows!")
        return df