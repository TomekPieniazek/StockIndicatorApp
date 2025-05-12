import pandas as pd
from strategies.base_strategy import BaseStrategy

class MeanReversionStrategy(BaseStrategy):
    def simulate(self, data: pd.DataFrame) -> pd.Series:
        last_return = data.pct_change().iloc[-1]
        return (-last_return).reindex(data.columns)