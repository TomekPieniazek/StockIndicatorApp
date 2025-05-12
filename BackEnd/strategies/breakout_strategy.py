import pandas as pd
from strategies.base_strategy import BaseStrategy

class BreakoutStrategy(BaseStrategy):
    def simulate(self, data: pd.DataFrame) -> pd.Series:
        high20 = data.rolling(window=20).max().iloc[-1]
        current = data.iloc[-1]
        breakout = (current - high20) / current
        return breakout.reindex(data.columns)