import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import warnings
import ta

warnings.filterwarnings("ignore")

portfolio = {
    "00878.TW": {"cost": 21.74, "shares": 200},
    "00919.TW": {"cost": 22.26, "shares": 400},
    "00924.TW": {"cost": 22.17, "shares": 100},
    "2330.TW":  {"cost": 900.20, "shares": 30},
    "2881.TW":  {"cost": 77.71, "shares": 100},
    "2891.TW":  {"cost": 42.96, "shares": 50},
    "6415.TW":  {"cost": 310.40, "shares": 10},
}

def fetch_basic_info(symbol):
    info = yf.Ticker(symbol).info
    pe = info.get("trailingPE")
    dy = info.get("dividendYield")
    beta = info.get("beta")
    if dy is not None:
        dy *= 100
    return pe, dy, beta

def add_technical_indicators(df):
    df["MA5"] = df["Close"].rolling(5).mean()
    df["MA10"] = df["Close"].rolling(10).mean()
    df["RSI"] = ta.momentum.rsi(df["Close"], window=14)
    macd = ta.trend.MACD(df["Close"])
    df["MACD"] = macd.macd()
    df["MACD_signal"] = macd.macd_signal()
    bb = ta.volatility.BollingerBands(df["Close"])
    df["BB_pctb"] = bb.bollinger_pband()
    stoch = ta.momentum.StochRSIIndicator(df["Close"])
    df["StochRSI"] = stoch.stochrsi()
    adx = ta.trend.ADXIndicator(df["High"], df["Low"], df["Close"], window=14)
    df["ADX"] = adx.adx()
    df["Volume_MA20"] = df["Volume"].rolling(20).mean()
    df["Pct_Chg_5"] = df["Close"].pct_change(5) * 100
    return df.dropna()

def forecast_with_indicators(symbol):
    df = yf.Ticker(symbol).history(period="1y")
    if df.empty or len(df) < 100:
        return None
    df = add_technical_indicators(df)
    df["Day"] = np.arange(len(df))
    X = df[["Day", "MA5", "MA10", "RSI", "MACD", "MACD_signal", "BB_pctb", "StochRSI", "ADX"]]
    y = df["Close"].values.ravel()
    model = LinearRegression().fit(X[:-5], y[:-5])
    preds = model.predict(X[-5:])
    return df, df["Close"].iloc[-1], preds

def analyze_portfolio():
    for symbol, info in portfolio.items():
        print(f"\n=== {symbol} ===")
        cost = info["cost"]
        basic = fetch_basic_info(symbol)
        df, today_price, preds = None, None, None
        try:
            df, today_price, preds = forecast_with_indicators(symbol)
        except Exception as e:
            print("預測失敗:", e)
            continue
        if df is None:
            print("資料不足")
            continue

        avg_pred = preds.mean()
        pe, dy, beta = basic

        latest = df.iloc[-1]
        prev = df.iloc[-2]

        tech_conds = {
            "RSI < 40 (超賣區，股價可能反彈)": latest["RSI"] < 40,
            "MACD金叉（多頭訊號）": (latest["MACD"] > latest["MACD_signal"]) and (prev["MACD"] < prev["MACD_signal"]),
            "收盤價 > MA10（日均線）": latest["Close"] > latest["MA10"],
            "成交量 > 20日均量": latest["Volume"] > latest["Volume_MA20"],
            "布林帶 %B < 0.2（股價接近下緣）": latest["BB_pctb"] < 0.2,
            "隨機RSI < 0.2（超賣訊號）": latest["StochRSI"] < 0.2,
            "ADX > 20（趨勢強）": latest["ADX"] > 20
        }
        fund_conds = {
            "殖利率 ≥ 3%（現金回報佳）": dy is not None and dy >= 3,
            "本益比 PE ≤ 20（估值合理）": pe is not None and pe <= 20,
            "Beta < 1（波動低於大盤）": beta is not None and beta < 1
        }

        tech_ok = sum(tech_conds.values())
        fund_ok = sum(fund_conds.values())

        suggest = ("✅ 建議補倉" if (avg_pred > cost and tech_ok >= 4 and fund_ok >= 2)
                   else "❌ 不建議補倉")

        print(f"今日收盤：{today_price:.2f}，未來5日平均預測價：{avg_pred:.2f}")
        print(f"你的成本價：{cost:.2f}")
        print(f"PE：{pe}, 殖利率：{dy}%, Beta：{beta}")
        print(f"技術條件成立數：{tech_ok}/7")
        for k, v in tech_conds.items():
            print(f"  - {k}: {'成立' if v else '不成立'}")
        print(f"基本面條件成立數：{fund_ok}/3")
        for k, v in fund_conds.items():
            print(f"  - {k}: {'成立' if v else '不成立'}")

        print("\n補倉建議：", suggest)
        print("說明：")
        if suggest == "✅ 建議補倉":
            print("- 預測價格高於成本價，具潛在獲利空間。")
            print("- 多項技術指標呈現買進訊號，例如超賣區、金叉及成交量增加。")
            print("- 基本面健康，估值合理且殖利率吸引。")
            print("- 風險指標Beta較低，波動相對穩定。")
        else:
            print("- 預測價格未顯著高於成本價，獲利空間有限或有下跌風險。")
            print("- 技術指標訊號不足，短期可能缺乏反彈動能。")
            print("- 基本面不佳或估值偏高，殖利率不具吸引力。")
            print("- Beta高於1，可能波動風險較大。")
        
        print("\n未來5天每日預測收盤價：")
        for i, p in enumerate(preds, 1):
            pct = (p - today_price) / today_price * 100
            print(f" Day+{i} 預測收盤：{p:.2f} ({pct:+.2f}%)")

if __name__ == "__main__":
    analyze_portfolio()
