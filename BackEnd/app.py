from flask import Flask, jsonify, request
import pandas as pd
import numpy as np

from strategies.momentum_strategy import MomentumStrategy
from strategies.mean_reversion_strategy import MeanReversionStrategy
from strategies.breakout_strategy import BreakoutStrategy
from strategies.volatility_strategy import VolatilityStrategy
from strategies.combined_strategy import CombinedStrategy
from backtester import Backtester
from pm import PortfolioManager
from cluster import ClusterManager
from utils.data_fetcher import DataFetcher

DEFAULT_PERIOD = "6mo"
SIGNAL_HIGH_THRESH = 0.02
SIGNAL_LOW_THRESH  = -0.02
DEFAULT_TICKERS = ["AAPL", "MSFT", "TSLA", "GOOG", "AMZN", "NFLX", "META"]

strategies = [
    MomentumStrategy(DEFAULT_TICKERS),
    MeanReversionStrategy(DEFAULT_TICKERS),
    BreakoutStrategy(DEFAULT_TICKERS),
    VolatilityStrategy(DEFAULT_TICKERS),
    CombinedStrategy(DEFAULT_TICKERS, weights=[0.6, 0.4]),
]

def _classify(score: float) -> str:
    if score >= SIGNAL_HIGH_THRESH:
        return "BUY"
    if score <= SIGNAL_LOW_THRESH:
        return "SELL"
    return "HOLD"

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return jsonify(
        message=(
            "Trading‑Signals API is up ✨. Endpoints: "
            "/signals, /backtest, /optimize, /cluster"
        )
    )

@app.route("/signals", methods=["GET"])
def signals():
    try:
        tickers = request.args.getlist("tickers") or DEFAULT_TICKERS
        data = DataFetcher.get_data(tickers, period=DEFAULT_PERIOD)

        frames = []
        for strat in strategies:
            s = strat.simulate(data).rename(type(strat).__name__)
            frames.append(s)

        score_df = pd.concat(frames, axis=1).reindex(index=tickers).fillna(0.0)
        agg = score_df.mean(axis=1)
        out = {t: _classify(float(v)) for t, v in agg.items()}
        return jsonify(out)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/backtest", methods=["GET"])
def backtest():
    try:
        bt = Backtester(strategies)
        res = bt.run(tickers=DEFAULT_TICKERS, period=DEFAULT_PERIOD)
        return jsonify(res.to_dict())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/optimize", methods=["POST"])
def optimize():
    try:
        body = request.get_json(silent=True) or {}
        generations = int(body.get("generations", 50))
        bt = Backtester(strategies)
        perf = bt.run(tickers=DEFAULT_TICKERS, period=DEFAULT_PERIOD).fillna(0).values
        pm = PortfolioManager(strategies)
        best_alloc = pm.run_ga(perf, generations=generations)
        return jsonify({"allocation": best_alloc.tolist()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/cluster", methods=["GET"])
def cluster():
    try:
        bt = Backtester(strategies)
        perf = bt.run(tickers=DEFAULT_TICKERS, period=DEFAULT_PERIOD).fillna(0).values.reshape(-1, 1)
        cm = ClusterManager(n_clusters=2)
        labels = cm.fit(perf)
        return jsonify({type(s).__name__: int(label) for s, label in zip(strategies, labels)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
