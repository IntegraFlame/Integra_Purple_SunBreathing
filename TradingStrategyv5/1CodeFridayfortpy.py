import yfinance as yf
import pandas as pd

tickers = ['SGOV', 'MO', 'SCHD', 'ABBV', 'JNJ', 'V', 'WMT']
data = {}
for t in tickers:
    try:
        ticker = yf.Ticker(t)
        hist = ticker.history(period="1mo")
        price = hist['Close'].iloc[-1]
        yield_pct = ticker.info.get('dividendYield', 0)
        if yield_pct is None:
            yield_pct = 0
        data[t] = {'Price': price, 'Yield': yield_pct * 100}
    except Exception as e:
        print(f"Error {t}: {e}")

df = pd.DataFrame(data).T
print(df)