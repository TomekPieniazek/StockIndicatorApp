import numpy as np
import pandas as pd
from strategies.base_strategy import BaseStrategy

class CombinedStrategy(BaseStrategy):
    def __init__(self, tickers, weights):
        super().__init__(tickers)
        self.weights = np.array(weights)
        if self.weights.size != 2:
            raise ValueError("CombinedStrategy expects exactly two weights")

    def simulate(self, data: pd.DataFrame) -> pd.Series:
        returns = data.pct_change()
        mom = returns.mean()
        rev = -returns.iloc[-1]
        signal = self.weights[0] * mom + self.weights[1] * rev
        return signal.reindex(data.columns)