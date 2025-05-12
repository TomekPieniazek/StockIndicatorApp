import pandas as pd
from strategies.base_strategy import BaseStrategy

class VolatilityStrategy(BaseStrategy):
    def simulate(self, data: pd.DataFrame) -> pd.Series:
        vol = data.pct_change().rolling(window=20).std().iloc[-1]
        inv_vol = 1 / vol.replace(0, pd.NA)
        return inv_vol.reindex(data.columns)