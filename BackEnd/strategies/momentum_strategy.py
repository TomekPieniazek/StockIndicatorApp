import pandas as pd
from strategies.base_strategy import BaseStrategy

class MomentumStrategy(BaseStrategy):
    def simulate(self, data: pd.DataFrame) -> pd.Series:
        returns = data.pct_change().rolling(window=20).mean().iloc[-1]
        return returns.reindex(data.columns)