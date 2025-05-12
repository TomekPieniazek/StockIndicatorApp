from abc import ABC, abstractmethod
import pandas as pd

class BaseStrategy(ABC):
    def __init__(self, tickers):
        self.tickers = tickers

    @abstractmethod
    def simulate(self, data: pd.DataFrame) -> pd.Series:
        pass