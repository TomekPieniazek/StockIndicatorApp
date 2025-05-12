import pandas as pd
from typing import List
from utils.data_fetcher import DataFetcher

class Backtester:
    def __init__(self, strategies):
        self.strategies = strategies

    def run(self, tickers: List[str], period="1y") -> pd.Series:
        data = DataFetcher.get_data(tickers, period=period)
        results = {}
        for strat in self.strategies:
            try:
                scores = strat.simulate(data).reindex(tickers)
                results[type(strat).__name__] = float(scores.mean())
            except Exception as e:
                print(f"[Backtester] error in {type(strat).__name__}: {e}")
                results[type(strat).__name__] = float('nan')
        return pd.Series(results, name='score')