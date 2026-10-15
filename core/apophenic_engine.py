import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from typing import Dict, Any, Optional, Tuple, Union


class AutonomousPatternConnectionEngine:
    """
    Apophenic Protocol: Universal Mathematical & Algorithmic Engine for Arbitrary Time-Series Assets.
    - Schema-Agnostic: Accepts file paths (CSV/Excel), DataFrames, Dicts, or 1D/2D Arrays.
    - Length-Agnostic (Unnamed N): Dynamically partitions N rows into geometric regime horizons.
    - Scale-Invariant: Uses log-return volatility to self-calibrate Directional-Change (ZigZag)
      thresholds across both Macro Cycles and Intermediate (3-6 wk) Sub-Waves.
    """

    def __init__(self, base_cycle_bars: int = 21, macro_mult: float = 1.65, interm_mult: float = 0.95):
        self.base_cycle_bars = base_cycle_bars
        self.macro_mult = macro_mult
        self.interm_mult = interm_mult

    @staticmethod
    def ingest_and_normalize(data_source: Union[str, pd.DataFrame, dict, np.ndarray, list]) -> pd.DataFrame:
        """Ingests any variable or file format and normalizes OHLCV and Date columns."""
        if isinstance(data_source, str):
            if data_source.lower().endswith(('.xls', '.xlsx')):
                xls = pd.ExcelFile(data_source)
                df = pd.read_excel(data_source, sheet_name=xls.sheet_names[0])
            else:
                df = pd.read_csv(data_source)
        elif isinstance(data_source, pd.DataFrame):
            df = data_source.copy()
        elif isinstance(data_source, (np.ndarray, list)):
            arr = np.asarray(data_source)
            df = pd.DataFrame({'Close': arr}) if arr.ndim == 1 else pd.DataFrame(arr)
        elif isinstance(data_source, dict):
            df = pd.DataFrame(data_source)
        else:
            raise ValueError("Unsupported data_source format.")

        col_map = {}
        for col in df.columns:
            c = str(col).strip().lower()
            if any(k in c for k in ['date', 'time', 'timestamp', 'dt']):
                col_map[col] = 'Date'
            elif any(k in c for k in ['close', 'last', 'adj', 'price', 'settle', 'nav']):
                col_map[col] = 'Close'
            elif 'open' in c:
                col_map[col] = 'Open'
            elif 'high' in c or 'max' in c:
                col_map[col] = 'High'
            elif 'low' in c or 'min' in c:
                col_map[col] = 'Low'
            elif 'vol' in c:
                col_map[col] = 'Volume'

        df = df.rename(columns=col_map)
        if 'Close' not in df.columns:
            num_cols = df.select_dtypes(include=[np.number]).columns
            df['Close'] = df[num_cols[0]]

        for c in ['Close', 'Open', 'High', 'Low', 'Volume']:
            if c in df.columns and df[c].dtype == object:
                df[c] = (
                    df[c]
                    .astype(str)
                    .str.replace('$', '', regex=False)
                    .str.replace(',', '', regex=False)
                    .str.replace('%', '', regex=False)
                )
                df[c] = pd.to_numeric(df[c], errors='coerce')

        df['High'] = df['High'].fillna(df['Close']) if 'High' in df.columns else df['Close']
        df['Low'] = df['Low'].fillna(df['Close']) if 'Low' in df.columns else df['Close']
        df['Open'] = df['Open'].fillna(df['Close']) if 'Open' in df.columns else df['Close']

        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
            df = df.dropna(subset=['Date', 'Close']).sort_values('Date').reset_index(drop=True)
        else:
            df = df.dropna(subset=['Close']).reset_index(drop=True)
            df['Date'] = pd.date_range(end=pd.Timestamp.today(), periods=len(df), freq='B')

        return df

    @staticmethod
    def compute_regime_horizons(df: pd.DataFrame) -> pd.DataFrame:
        """Partitions an unnamed length N into 5 geometric regime horizons."""
        n = len(df)
        slices = [
            ('Full_Dataset (100% N)', df),
            ('Half_Dataset (50% N)', df.tail(max(2, n // 2))),
            ('Quarter_Dataset (25% N)', df.tail(max(2, n // 4))),
            ('Trailing_1Y (min(252, N))', df.tail(min(252, n))),
            ('Active_Wave (min(63, N))', df.tail(min(63, n))),
        ]
        rows = []
        for name, sub in slices:
            c = sub['Close']
            rows.append({
                'Horizon': name,
                'Count': len(sub),
                'Mean': round(float(c.mean()), 4),
                'Median': round(float(c.median()), 4),
                'Min_Low': round(float(sub['Low'].min()), 4),
                'Max_High': round(float(sub['High'].max()), 4),
                'Std_Dev': round(float(c.std()), 4),
            })
        return pd.DataFrame(rows)

    @staticmethod
    def directional_change_graph(df: pd.DataFrame, tau_pct: float) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Connects alternating Peak -> Trough resets and Trough -> Peak impulses across N bars."""
        highs, lows, closes, dates = (
            df['High'].values,
            df['Low'].values,
            df['Close'].values,
            df['Date'].values,
        )
        pivots = []
        mode = 'SEARCH_PEAK'
        max_i, min_i = 0, 0

        for i in range(len(df)):
            if mode == 'SEARCH_PEAK':
                if highs[i] >= highs[max_i]:
                    max_i = i
                elif (highs[max_i] - lows[i]) / highs[max_i] >= tau_pct:
                    pivots.append({
                        'idx': max_i,
                        'Date': pd.Timestamp(dates[max_i]),
                        'Type': 'PEAK',
                        'Price': float(highs[max_i]),
                        'Close': float(closes[max_i]),
                    })
                    min_i = i
                    mode = 'SEARCH_TROUGH'
            else:
                if lows[i] <= lows[min_i]:
                    min_i = i
                elif (highs[i] - lows[min_i]) / lows[min_i] >= tau_pct:
                    pivots.append({
                        'idx': min_i,
                        'Date': pd.Timestamp(dates[min_i]),
                        'Type': 'TROUGH',
                        'Price': float(lows[min_i]),
                        'Close': float(closes[min_i]),
                    })
                    max_i = i
                    mode = 'SEARCH_PEAK'

        if mode == 'SEARCH_TROUGH':
            pivots.append({
                'idx': min_i,
                'Date': pd.Timestamp(dates[min_i]),
                'Type': 'TROUGH',
                'Price': float(lows[min_i]),
                'Close': float(closes[min_i]),
            })
        else:
            pivots.append({
                'idx': max_i,
                'Date': pd.Timestamp(dates[max_i]),
                'Type': 'PEAK',
                'Price': float(highs[max_i]),
                'Close': float(closes[max_i]),
            })

        resets, impulses = [], []
        for j in range(1, len(pivots)):
            p0, p1 = pivots[j - 1], pivots[j]
            bars = p1['idx'] - p0['idx']
            if p0['Type'] == 'PEAK' and p1['Type'] == 'TROUGH':
                resets.append({
                    'Peak_Date': p0['Date'],
                    'Peak_High': p0['Price'],
                    'Peak_Close': p0['Close'],
                    'Trough_Date': p1['Date'],
                    'Trough_Low': p1['Price'],
                    'Trough_Close': p1['Close'],
                    'Dollar_Drop': p0['Price'] - p1['Price'],
                    'Close_Drop': p0['Close'] - p1['Close'],
                    'Pct_Drop': (p1['Price'] - p0['Price']) / p0['Price'],
                    'Bars': bars,
                })
            elif p0['Type'] == 'TROUGH' and p1['Type'] == 'PEAK':
                impulses.append({
                    'Trough_Date': p0['Date'],
                    'Trough_Low': p0['Price'],
                    'Peak_Date': p1['Date'],
                    'Peak_High': p1['Price'],
                    'Dollar_Gain': p1['Price'] - p0['Price'],
                    'Pct_Gain': (p1['Price'] - p0['Price']) / p0['Price'],
                    'Bars': bars,
                })
        return pd.DataFrame(resets), pd.DataFrame(impulses)

    def execute_pipeline(
        self,
        data_source: Any,
        entry_price: Optional[float] = None,
        lookback_cycles: int = 8,
    ) -> Dict[str, Any]:
        """Executes the full 6-stage Apophenic Protocol mathematical pipeline."""
        df = self.ingest_and_normalize(data_source)
        n = len(df)
        spot = float(df['Close'].iloc[-1])

        log_ret = np.log(df['Close'] / df['Close'].shift(1)).dropna()
        sigma_daily = float(log_ret.std())
        tau_macro = max(0.025, self.macro_mult * sigma_daily * np.sqrt(self.base_cycle_bars))
        tau_interm = max(0.015, self.interm_mult * sigma_daily * np.sqrt(self.base_cycle_bars))

        macro_resets, macro_impulses = self.directional_change_graph(df, tau_macro)
        interm_resets, interm_impulses = self.directional_change_graph(df, tau_interm)

        rec_resets = macro_resets.tail(lookback_cycles)
        rec_interm_imp = interm_impulses.tail(lookback_cycles)

        med_drop_dlr = float(rec_resets['Dollar_Drop'].median())
        mean_drop_dlr = float(rec_resets['Dollar_Drop'].mean())
        med_drop_pct = float(rec_resets['Pct_Drop'].median())

        interm_gain_dlr = float(rec_interm_imp['Dollar_Gain'].median())
        interm_gain_pct = float(rec_interm_imp['Pct_Gain'].median())

        ma_dict = {
            f"SMA_{w}": round(float(df['Close'].rolling(w).mean().iloc[-1]), 4)
            for w in [9, 20, 50, 100, 200]
            if w < n
        }

        reg_bars = min(197, n)
        sub_reg = df.tail(reg_bars)
        t_vec = np.arange(reg_bars)
        slope, intercept = np.polyfit(t_vec, sub_reg['Close'].values, 1)
        resid_95 = float(np.percentile(sub_reg['High'].values - (intercept + slope * t_vec), 95))
        channel_ceiling = float((intercept + slope * (reg_bars + self.base_cycle_bars)) + resid_95)

        anchor_trough = (
            float(interm_resets['Trough_Low'].iloc[-1])
            if not interm_resets.empty
            else float(df['Low'].tail(21).min())
        )
        proj_peak_dlr = anchor_trough + interm_gain_dlr
        proj_peak_pct = anchor_trough * (1.0 + interm_gain_pct)

        sell_low = round(min(proj_peak_dlr, proj_peak_pct), 2)
        sell_high = round(min(max(proj_peak_dlr, proj_peak_pct), channel_ceiling), 2)
        sell_point = round(0.5 * (sell_low + sell_high), 2)

        buyback_low = round(sell_point - mean_drop_dlr, 2)
        buyback_high = round(sell_point - med_drop_dlr, 2)
        buyback_point = round(0.5 * (buyback_low + buyback_high), 2)

        min_peak_for_core = round((entry_price + med_drop_dlr), 2) if entry_price else None
        verdict = (
            "SELL_100%_AT_PEAK_AND_REBUY"
            if (entry_price and buyback_point <= entry_price)
            else "HOLD_50%_CORE_TRIM_50%"
        )

        return {
            'Dataset_Rows_N': n,
            'Current_Spot': round(spot, 4),
            'Adaptive_Thresholds': {
                'Macro_Tau_Pct': round(tau_macro * 100, 2),
                'Interm_Tau_Pct': round(tau_interm * 100, 2),
            },
            'Regime_Horizons': self.compute_regime_horizons(df).to_dict(orient='records'),
            'Moving_Averages': ma_dict,
            'Connected_Cycle_Metrics': {
                'Macro_Resets_Count': len(macro_resets),
                'Interm_Waves_Count': len(interm_impulses),
                'Recent_Median_Peak_Drop_($)': round(med_drop_dlr, 4),
                'Recent_Mean_Peak_Drop_($)': round(mean_drop_dlr, 4),
                'Recent_Median_Peak_Drop_(%)': round(med_drop_pct * 100, 2),
                'Recent_Interm_Impulse_Gain_($)': round(interm_gain_dlr, 4),
                'Recent_Interm_Impulse_Gain_(%)': round(interm_gain_pct * 100, 2),
            },
            'Connected_Projections': {
                'Last_Confirmed_Trough_($)': round(anchor_trough, 2),
                'Projected_Sell_Band_($)': (sell_low, sell_high),
                'Optimal_Sell_Threshold_($)': sell_point,
                'Projected_Buyback_Band_($)': (buyback_low, buyback_high),
                'Optimal_Buyback_Threshold_($)': buyback_point,
                'Min_Peak_Required_For_50%_Hold_($)': min_peak_for_core,
                'Execution_Verdict': verdict,
            },
            'Recent_Resets_Table': rec_resets.to_dict(orient='records'),
        }
