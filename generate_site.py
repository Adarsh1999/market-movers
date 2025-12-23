#!/usr/bin/env python3
"""
S&P 500 Market Movers - Static Site Generator
Generates a beautiful static website with daily market data
"""

import os
import json
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta, timezone, date
from zoneinfo import ZoneInfo
import warnings

# S&P 500 tickers (comprehensive list)
SP500_TICKERS = [
    'A', 'AAPL', 'ABBV', 'ABNB', 'ABT', 'ACGL', 'ACN', 'ADBE', 'ADI', 'ADM',
    'ADP', 'ADSK', 'AEE', 'AEP', 'AES', 'AFL', 'AIG', 'AIZ', 'AJG', 'AKAM',
    'ALB', 'ALGN', 'ALL', 'ALLE', 'AMAT', 'AMCR', 'AMD', 'AME', 'AMGN', 'AMP',
    'AMT', 'AMZN', 'ANET', 'AON', 'AOS', 'APA', 'APD', 'APH', 'APO', 'APP',
    'APTV', 'ARE', 'ARES', 'ATO', 'AVB', 'AVGO', 'AVY', 'AWK', 'AXON', 'AXP',
    'AZO', 'BA', 'BAC', 'BALL', 'BAX', 'BBY', 'BDX', 'BEN', 'BF-B', 'BG',
    'BIIB', 'BK', 'BKNG', 'BKR', 'BLDR', 'BLK', 'BMY', 'BR', 'BRK-B', 'BRO',
    'BSX', 'BX', 'BXP', 'C', 'CAG', 'CAH', 'CARR', 'CAT', 'CB', 'CBOE',
    'CBRE', 'CCI', 'CCL', 'CDNS', 'CDW', 'CEG', 'CF', 'CFG', 'CHD', 'CHRW',
    'CHTR', 'CI', 'CINF', 'CL', 'CLX', 'CMCSA', 'CME', 'CMG', 'CMI', 'CMS',
    'CNC', 'CNP', 'COF', 'COIN', 'COO', 'COP', 'COR', 'COST', 'CPAY', 'CPB',
    'CPRT', 'CPT', 'CRL', 'CRM', 'CRWD', 'CSCO', 'CSGP', 'CSX', 'CTAS', 'CTRA',
    'CTSH', 'CTVA', 'CVS', 'CVX', 'D', 'DAL', 'DASH', 'DAY', 'DD', 'DDOG',
    'DE', 'DECK', 'DELL', 'DG', 'DGX', 'DHI', 'DHR', 'DIS', 'DLR', 'DLTR',
    'DOC', 'DOV', 'DOW', 'DPZ', 'DRI', 'DTE', 'DUK', 'DVA', 'DVN', 'DXCM',
    'EA', 'EBAY', 'ECL', 'ED', 'EFX', 'EG', 'EIX', 'EL', 'ELV', 'EME',
    'EMR', 'EOG', 'EPAM', 'EQIX', 'EQR', 'EQT', 'ERIE', 'ES', 'ESS', 'ETN',
    'ETR', 'EVRG', 'EW', 'EXC', 'EXE', 'EXPD', 'EXPE', 'EXR', 'F', 'FANG',
    'FAST', 'FCX', 'FDS', 'FDX', 'FE', 'FFIV', 'FICO', 'FIS', 'FISV', 'FITB',
    'FOX', 'FOXA', 'FRT', 'FSLR', 'FTNT', 'FTV', 'GD', 'GDDY', 'GE', 'GEHC',
    'GEN', 'GEV', 'GILD', 'GIS', 'GL', 'GLW', 'GM', 'GNRC', 'GOOG', 'GOOGL',
    'GPC', 'GPN', 'GRMN', 'GS', 'GWW', 'HAL', 'HAS', 'HBAN', 'HCA', 'HD',
    'HIG', 'HII', 'HLT', 'HOLX', 'HON', 'HOOD', 'HPE', 'HPQ', 'HRL', 'HSIC',
    'HST', 'HSY', 'HUBB', 'HUM', 'HWM', 'IBKR', 'IBM', 'ICE', 'IDXX', 'IEX',
    'IFF', 'INCY', 'INTC', 'INTU', 'INVH', 'IP', 'IQV', 'IR', 'IRM', 'ISRG',
    'IT', 'ITW', 'IVZ', 'J', 'JBHT', 'JBL', 'JCI', 'JKHY', 'JNJ', 'JPM',
    'KDP', 'KEY', 'KEYS', 'KHC', 'KIM', 'KKR', 'KLAC', 'KMB', 'KMI', 'KO',
    'KR', 'KVUE', 'L', 'LDOS', 'LEN', 'LH', 'LHX', 'LII', 'LIN', 'LKQ',
    'LLY', 'LMT', 'LNT', 'LOW', 'LRCX', 'LULU', 'LUV', 'LVS', 'LW', 'LYB',
    'LYV', 'MA', 'MAA', 'MAR', 'MAS', 'MCD', 'MCHP', 'MCK', 'MCO', 'MDLZ',
    'MDT', 'MET', 'META', 'MGM', 'MHK', 'MKC', 'MLM', 'MMC', 'MMM', 'MNST',
    'MO', 'MOH', 'MOS', 'MPC', 'MPWR', 'MRK', 'MRNA', 'MS', 'MSCI', 'MSFT',
    'MSI', 'MTB', 'MTCH', 'MTD', 'MU', 'NCLH', 'NDAQ', 'NDSN', 'NEE', 'NEM',
    'NFLX', 'NI', 'NKE', 'NOC', 'NOW', 'NRG', 'NSC', 'NTAP', 'NTRS', 'NUE',
    'NVDA', 'NVR', 'NWS', 'NWSA', 'NXPI', 'O', 'ODFL', 'OKE', 'OMC', 'ON',
    'ORCL', 'ORLY', 'OTIS', 'OXY', 'PANW', 'PAYC', 'PAYX', 'PCAR', 'PCG', 'PEG',
    'PEP', 'PFE', 'PFG', 'PG', 'PGR', 'PH', 'PHM', 'PKG', 'PLD', 'PLTR',
    'PM', 'PNC', 'PNR', 'PNW', 'PODD', 'POOL', 'PPG', 'PPL', 'PRU', 'PSA',
    'PSKY', 'PSX', 'PTC', 'PWR', 'PYPL', 'Q', 'QCOM', 'RCL', 'REG', 'REGN',
    'RF', 'RJF', 'RL', 'RMD', 'ROK', 'ROL', 'ROP', 'ROST', 'RSG', 'RTX',
    'RVTY', 'SBAC', 'SBUX', 'SCHW', 'SHW', 'SJM', 'SLB', 'SMCI', 'SNA', 'SNDK',
    'SNPS', 'SO', 'SOLS', 'SOLV', 'SPG', 'SPGI', 'SRE', 'STE', 'STLD', 'STT',
    'STX', 'STZ', 'SW', 'SWK', 'SWKS', 'SYF', 'SYK', 'SYY', 'T', 'TAP',
    'TDG', 'TDY', 'TECH', 'TEL', 'TER', 'TFC', 'TGT', 'TJX', 'TKO', 'TMO',
    'TMUS', 'TPL', 'TPR', 'TRGP', 'TRMB', 'TROW', 'TRV', 'TSCO', 'TSLA', 'TSN',
    'TT', 'TTD', 'TTWO', 'TXN', 'TXT', 'TYL', 'UAL', 'UBER', 'UDR', 'UHS',
    'ULTA', 'UNH', 'UNP', 'UPS', 'URI', 'USB', 'V', 'VICI', 'VLO', 'VLTO',
    'VMC', 'VRSK', 'VRSN', 'VRTX', 'VST', 'VTR', 'VTRS', 'VZ', 'WAB', 'WAT',
    'WBD', 'WDAY', 'WDC', 'WEC', 'WELL', 'WFC', 'WM', 'WMB', 'WMT', 'WRB',
    'WSM', 'WST', 'WTW', 'WY', 'WYNN', 'XEL', 'XOM', 'XYL', 'XYZ', 'YUM',
    'ZBH', 'ZBRA', 'ZTS',
]

CHART_PERIOD = "1y"
CHART_DAY_BARS = 60
CHART_WEEK_BARS = 26
CHART_MONTH_BARS = 12

# Intraday chart settings
CHART_15M_BARS = 160   # ~5 trading days of 15-min bars
CHART_1H_BARS = 195    # ~30 trading days of 1-hour bars
CHART_2H_BARS = 98     # ~30 trading days of 2-hour bars
CHART_3H_BARS = 65     # ~30 trading days of 3-hour bars



def download_sp500_history(period: str = "10d"):
    """Download recent history for all S&P 500 stocks using yfinance.

    We download once and derive both daily + weekly datasets from the same data.
    """
    print(f"Downloading {period} of data for {len(SP500_TICKERS)} S&P 500 stocks...")
    tickers_str = " ".join(SP500_TICKERS)

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return yf.download(
            tickers_str,
            period=period,
            progress=False,
            threads=True,
            auto_adjust=True,
            ignore_tz=True,
        )


def download_chart_history(tickers, period: str = CHART_PERIOD):
    """Download OHLC history for charting the selected tickers."""
    if not tickers:
        return None

    print(f"Downloading {period} of chart data for {len(tickers)} tickers...")
    tickers_str = " ".join(tickers)

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return yf.download(
            tickers_str,
            period=period,
            interval="1d",
            progress=False,
            threads=True,
            auto_adjust=True,
            ignore_tz=True,
        )


def download_intraday_15m(tickers):
    """Download 15-minute intraday data (last 60 days max from Yahoo)."""
    if not tickers:
        return None

    print(f"Downloading 15-min intraday data for {len(tickers)} tickers...")
    tickers_str = " ".join(tickers)

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return yf.download(
            tickers_str,
            period="5d",  # ~5 trading days of 15-min data
            interval="15m",
            progress=False,
            threads=True,
            auto_adjust=True,
            ignore_tz=True,
        )


def download_intraday_1h(tickers):
    """Download 1-hour intraday data (last 730 days max from Yahoo)."""
    if not tickers:
        return None

    print(f"Downloading 1-hour intraday data for {len(tickers)} tickers...")
    tickers_str = " ".join(tickers)

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return yf.download(
            tickers_str,
            period="1mo",  # ~30 trading days of hourly data
            interval="1h",
            progress=False,
            threads=True,
            auto_adjust=True,
            ignore_tz=True,
        )


def _series_for_field(data, field: str, ticker: str):
    try:
        return data[field][ticker].dropna()
    except Exception:
        try:
            return data[field].dropna()
        except Exception:
            return None


def _build_ohlc_frame(data, ticker: str) -> pd.DataFrame | None:
    open_series = _series_for_field(data, "Open", ticker)
    high_series = _series_for_field(data, "High", ticker)
    low_series = _series_for_field(data, "Low", ticker)
    close_series = _series_for_field(data, "Close", ticker)

    if open_series is None or high_series is None or low_series is None or close_series is None:
        return None

    frame = pd.DataFrame(
        {
            "open": open_series,
            "high": high_series,
            "low": low_series,
            "close": close_series,
        }
    )
    frame = frame.dropna()
    frame = frame.sort_index()
    return frame


def _resample_ohlc(frame: pd.DataFrame, rule: str) -> pd.DataFrame:
    resampled = frame.resample(rule).agg(
        {
            "open": "first",
            "high": "max",
            "low": "min",
            "close": "last",
        }
    )
    return resampled.dropna(subset=["open", "close"])


def _format_candles(frame: pd.DataFrame, max_bars: int, use_datetime: bool = False) -> list[dict]:
    """Format candles for chart display.
    
    Args:
        frame: DataFrame with OHLC data
        max_bars: Maximum number of bars to return
        use_datetime: If True, use full datetime for timestamp (for intraday).
                     If False, use date only (for daily/weekly/monthly).
    """
    if frame.empty:
        return []

    frame = frame.tail(max_bars)
    candles = []
    for idx, row in frame.iterrows():
        if use_datetime:
            # For intraday data, use the full datetime
            if hasattr(idx, 'timestamp'):
                candle_time = int(idx.timestamp())
            else:
                candle_time = int(datetime.combine(idx.date(), datetime.min.time(), tzinfo=timezone.utc).timestamp())
        else:
            # For daily/weekly/monthly, use date at midnight UTC
            candle_time = datetime.combine(idx.date(), datetime.min.time(), tzinfo=timezone.utc)
            candle_time = int(candle_time.timestamp())
        
        candles.append(
            {
                "time": candle_time,
                "open": float(row["open"]),
                "high": float(row["high"]),
                "low": float(row["low"]),
                "close": float(row["close"]),
            }
        )
    return candles


def _format_intraday_candles(frame: pd.DataFrame, max_bars: int) -> list[dict]:
    """Format intraday candles preserving full timestamp."""
    return _format_candles(frame, max_bars, use_datetime=True)


def build_chart_payloads(data, tickers, data_15m=None, data_1h=None) -> dict:
    """Build chart payloads with daily, weekly, monthly, and intraday data.
    
    Args:
        data: Daily OHLC data
        tickers: List of ticker symbols
        data_15m: Optional 15-minute intraday data
        data_1h: Optional 1-hour intraday data
    """
    payloads = {}
    if data is None:
        return payloads

    for ticker in tickers:
        # Daily/Weekly/Monthly from daily data
        frame = _build_ohlc_frame(data, ticker)
        if frame is None or frame.empty:
            continue

        daily = _format_candles(frame, CHART_DAY_BARS)
        weekly = _format_candles(_resample_ohlc(frame, "W-FRI"), CHART_WEEK_BARS)
        monthly = _format_candles(_resample_ohlc(frame, "M"), CHART_MONTH_BARS)

        payload = {
            "ticker": ticker,
            "day": daily,
            "week": weekly,
            "month": monthly,
            "m15": [],
            "h1": [],
            "h2": [],
            "h3": [],
        }

        # 15-minute data
        if data_15m is not None:
            frame_15m = _build_ohlc_frame(data_15m, ticker)
            if frame_15m is not None and not frame_15m.empty:
                payload["m15"] = _format_intraday_candles(frame_15m, CHART_15M_BARS)

        # 1-hour data and resampled 2h/3h
        if data_1h is not None:
            frame_1h = _build_ohlc_frame(data_1h, ticker)
            if frame_1h is not None and not frame_1h.empty:
                payload["h1"] = _format_intraday_candles(frame_1h, CHART_1H_BARS)
                # Resample to 2-hour and 3-hour
                frame_2h = _resample_ohlc(frame_1h, "2h")
                frame_3h = _resample_ohlc(frame_1h, "3h")
                payload["h2"] = _format_intraday_candles(frame_2h, CHART_2H_BARS)
                payload["h3"] = _format_intraday_candles(frame_3h, CHART_3H_BARS)

        payloads[ticker] = payload

    return payloads


def write_chart_payloads(payloads: dict, output_dir: str):
    if not payloads:
        return

    os.makedirs(output_dir, exist_ok=True)
    for ticker, payload in payloads.items():
        path = os.path.join(output_dir, f"{ticker}.json")
        with open(path, "w") as f:
            json.dump(payload, f)

def build_daily_dataset(data):
    """Build daily dataset from downloaded history (last 2 closes)."""
    results = []

    for ticker in SP500_TICKERS:
        try:
            close_prices = data["Close"][ticker].dropna()
            if len(close_prices) < 2:
                continue

            prev_close = float(close_prices.iloc[-2])
            current_close = float(close_prices.iloc[-1])
            if prev_close == 0 or current_close == 0:
                continue

            change = current_close - prev_close
            change_pct = (change / prev_close) * 100

            volume_series = data["Volume"][ticker].dropna()
            volume = int(volume_series.iloc[-1]) if len(volume_series) > 0 else 0

            results.append(
                {
                    "ticker": ticker,
                    "price": round(current_close, 2),
                    "prev_close": round(prev_close, 2),
                    "change": round(change, 2),
                    "change_pct": round(change_pct, 2),
                    "volume": volume if volume > 0 else 0,
                }
            )
        except Exception:
            continue

    dates = list(getattr(data, "index", []))
    meta = {
        "mode": "daily",
        "trading_days_available": len(dates),
    }
    if len(dates) >= 2:
        meta["start_date"] = dates[-2].date().isoformat()
        meta["end_date"] = dates[-1].date().isoformat()
    elif len(dates) == 1:
        meta["end_date"] = dates[-1].date().isoformat()

    print(f"Built daily dataset for {len(results)} stocks")
    return results, meta


def get_week_date_range(reference_dt: datetime) -> tuple[date, date]:
    """Return the completed Mon-Fri range for weekly reporting."""
    current_date = reference_dt.date()
    weekday = current_date.weekday()  # Monday=0, Sunday=6
    week_start = current_date - timedelta(days=weekday)

    # Sat/Sun -> current week; Mon-Fri -> previous week
    if weekday >= 5:
        start_date = week_start
    else:
        start_date = week_start - timedelta(days=7)

    end_date = start_date + timedelta(days=4)
    return start_date, end_date


def build_weekly_dataset(data, start_date: date, end_date: date):
    """Build weekly dataset from downloaded history (Mon-Fri date range)."""
    results = []

    for ticker in SP500_TICKERS:
        try:
            close_prices = data["Close"][ticker].dropna()
            if len(close_prices) < 2:
                continue

            trading_days = close_prices[
                (close_prices.index.date >= start_date) & (close_prices.index.date <= end_date)
            ]
            if len(trading_days) < 2:
                continue

            start_price = float(trading_days.iloc[0])
            end_price = float(trading_days.iloc[-1])
            if start_price == 0 or end_price == 0:
                continue

            change = end_price - start_price
            change_pct = (change / start_price) * 100

            volume_series = data["Volume"][ticker].dropna()
            volume_series = volume_series[
                (volume_series.index.date >= start_date) & (volume_series.index.date <= end_date)
            ]
            avg_volume = int(volume_series.mean()) if len(volume_series) > 0 else 0

            results.append(
                {
                    "ticker": ticker,
                    "start_price": round(start_price, 2),
                    "end_price": round(end_price, 2),
                    "change": round(change, 2),
                    "change_pct": round(change_pct, 2),
                    "avg_volume": avg_volume if avg_volume > 0 else 0,
                    "days": int(len(trading_days)),
                }
            )
        except Exception:
            continue

    dates = list(getattr(data, "index", []))
    dates_in_range = [d for d in dates if start_date <= d.date() <= end_date]
    meta = {
        "mode": "weekly",
        "trading_days_available": len(dates_in_range),
    }
    meta["start_date"] = start_date.isoformat()
    meta["end_date"] = end_date.isoformat()

    print(f"Built weekly dataset for {len(results)} stocks")
    return results, meta


def get_top_movers(stocks, limit=20):
    """Get top gainers and losers from the stock list"""
    sorted_stocks = sorted(stocks, key=lambda x: x['change_pct'], reverse=True)
    
    gainers = [s for s in sorted_stocks if s['change_pct'] > 0][:limit]
    losers = [s for s in sorted_stocks if s['change_pct'] < 0][-limit:]
    losers.reverse()
    
    return gainers, losers


def generate_daily_csv(stocks, filename):
    """Generate daily CSV file for download (Excel-friendly)."""
    import csv
    
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Rank', 'Symbol', 'Price ($)', 'Previous Close ($)', 'Change ($)', 'Change (%)', 'Volume'])
        for i, stock in enumerate(stocks, 1):
            writer.writerow([
                i,
                stock['ticker'],
                stock['price'],
                stock['prev_close'],
                stock['change'],
                f"{stock['change_pct']:+.2f}%",
                stock['volume']
            ])
    print(f"Generated {filename}")


def generate_weekly_csv(stocks, filename):
    """Generate weekly CSV file for download (Excel-friendly)."""
    import csv

    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "Rank",
                "Symbol",
                "Week Start ($)",
                "Week End ($)",
                "Change ($)",
                "Change (%)",
                "Avg Volume",
                "Days",
            ]
        )
        for i, stock in enumerate(stocks, 1):
            writer.writerow(
                [
                    i,
                    stock["ticker"],
                    stock["start_price"],
                    stock["end_price"],
                    stock["change"],
                    f"{stock['change_pct']:+.2f}%",
                    stock.get("avg_volume", 0),
                    stock.get("days", 0),
                ]
            )
    print(f"Generated {filename}")


def _pretty_date(iso_date: str, fmt: str = "%b %d, %Y") -> str:
    try:
        if not iso_date:
            return ""
        return date.fromisoformat(iso_date).strftime(fmt)
    except Exception:
        return iso_date


def generate_html(
    daily_gainers,
    daily_losers,
    daily_all_stocks,
    daily_meta,
    weekly_gainers,
    weekly_losers,
    weekly_all_stocks,
    weekly_meta,
    generated_at_et: datetime,
):
    """Generate the main HTML page (Daily + Weekly views)."""

    generated_str = generated_at_et.strftime("%b %d, %Y %I:%M %p %Z")

    daily_end_str = _pretty_date(daily_meta.get("end_date", ""))
    weekly_start_str = _pretty_date(weekly_meta.get("start_date", ""))
    weekly_end_str = _pretty_date(weekly_meta.get("end_date", ""))

    daily_update_label = f"Daily data: {daily_end_str} • Generated: {generated_str}"
    weekly_update_label = f"Weekly (Mon-Fri): {weekly_start_str} - {weekly_end_str} • Generated: {generated_str}"

    daily_subtitle = "Daily Top Gainers & Losers"
    weekly_subtitle = "Weekly Movers (Mon-Fri)"
    default_view = "weekly" if (generated_at_et.weekday() >= 5 and len(weekly_all_stocks) > 0) else "daily"

    # Generate table rows for DAILY gainers
    daily_gainers_rows = ""
    for i, stock in enumerate(daily_gainers, 1):
        daily_gainers_rows += f'''
            <tr class="clickable-row" data-ticker="{stock['ticker']}" tabindex="0" role="button" aria-label="Open chart for {stock['ticker']}">
                <td class="rank">{i}</td>
                <td class="symbol">{stock['ticker']}</td>
                <td class="price">${stock['price']:.2f}</td>
                <td class="change positive">+${stock['change']:.2f}</td>
                <td class="change-pct positive">+{stock['change_pct']:.2f}%</td>
                <td class="volume">{stock['volume']:,}</td>
            </tr>'''

    # Generate table rows for DAILY losers
    daily_losers_rows = ""
    for i, stock in enumerate(daily_losers, 1):
        daily_losers_rows += f'''
            <tr class="clickable-row" data-ticker="{stock['ticker']}" tabindex="0" role="button" aria-label="Open chart for {stock['ticker']}">
                <td class="rank">{i}</td>
                <td class="symbol">{stock['ticker']}</td>
                <td class="price">${stock['price']:.2f}</td>
                <td class="change negative">${stock['change']:.2f}</td>
                <td class="change-pct negative">{stock['change_pct']:.2f}%</td>
                <td class="volume">{stock['volume']:,}</td>
            </tr>'''

    # Generate table rows for WEEKLY gainers
    weekly_gainers_rows = ""
    for i, stock in enumerate(weekly_gainers, 1):
        weekly_gainers_rows += f'''
            <tr class="clickable-row" data-ticker="{stock['ticker']}" tabindex="0" role="button" aria-label="Open chart for {stock['ticker']}">
                <td class="rank">{i}</td>
                <td class="symbol">{stock['ticker']}</td>
                <td class="price">${stock['start_price']:.2f}</td>
                <td class="price">${stock['end_price']:.2f}</td>
                <td class="change positive">+${stock['change']:.2f}</td>
                <td class="change-pct positive">+{stock['change_pct']:.2f}%</td>
                <td class="volume">{stock.get('avg_volume', 0):,}</td>
            </tr>'''

    # Generate table rows for WEEKLY losers
    weekly_losers_rows = ""
    for i, stock in enumerate(weekly_losers, 1):
        weekly_losers_rows += f'''
            <tr class="clickable-row" data-ticker="{stock['ticker']}" tabindex="0" role="button" aria-label="Open chart for {stock['ticker']}">
                <td class="rank">{i}</td>
                <td class="symbol">{stock['ticker']}</td>
                <td class="price">${stock['start_price']:.2f}</td>
                <td class="price">${stock['end_price']:.2f}</td>
                <td class="change negative">${stock['change']:.2f}</td>
                <td class="change-pct negative">{stock['change_pct']:.2f}%</td>
                <td class="volume">{stock.get('avg_volume', 0):,}</td>
            </tr>'''

    # Calculate market summary (DAILY)
    daily_total_gainers = len([s for s in daily_all_stocks if s["change_pct"] > 0])
    daily_total_losers = len([s for s in daily_all_stocks if s["change_pct"] < 0])
    daily_total_unchanged = len(daily_all_stocks) - daily_total_gainers - daily_total_losers
    daily_avg_change = (
        sum(s["change_pct"] for s in daily_all_stocks) / len(daily_all_stocks) if daily_all_stocks else 0
    )
    daily_avg_class = "gainers" if daily_avg_change >= 0 else "losers"

    # Calculate market summary (WEEKLY)
    weekly_total_gainers = len([s for s in weekly_all_stocks if s["change_pct"] > 0])
    weekly_total_losers = len([s for s in weekly_all_stocks if s["change_pct"] < 0])
    weekly_total_unchanged = len(weekly_all_stocks) - weekly_total_gainers - weekly_total_losers
    weekly_avg_change = (
        sum(s["change_pct"] for s in weekly_all_stocks) / len(weekly_all_stocks) if weekly_all_stocks else 0
    )
    weekly_avg_class = "gainers" if weekly_avg_change >= 0 else "losers"

    # Convert data to JSON for JavaScript
    daily_all_stocks_json = json.dumps(daily_all_stocks)
    daily_gainers_json = json.dumps(daily_gainers)
    daily_losers_json = json.dumps(daily_losers)
    weekly_all_stocks_json = json.dumps(weekly_all_stocks)
    weekly_gainers_json = json.dumps(weekly_gainers)
    weekly_losers_json = json.dumps(weekly_losers)
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>S&P 500 Market Movers | Daily & Weekly Performance</title>
    <meta name="description" content="Daily and weekly S&P 500 top gainers and losers. Track the biggest market movers with downloadable reports.">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Outfit:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-primary: #0a0a0f;
            --bg-secondary: #12121a;
            --bg-card: #1a1a24;
            --bg-hover: #22222e;
            --text-primary: #f0f0f5;
            --text-secondary: #8888a0;
            --text-muted: #5a5a70;
            --accent-green: #00ff88;
            --accent-green-dim: #00cc6a;
            --accent-red: #ff3366;
            --accent-red-dim: #cc2952;
            --accent-blue: #00aaff;
            --accent-purple: #aa66ff;
            --border-color: #2a2a3a;
            --glow-green: 0 0 20px rgba(0, 255, 136, 0.3);
            --glow-red: 0 0 20px rgba(255, 51, 102, 0.3);
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Outfit', sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            min-height: 100vh;
            line-height: 1.6;
        }}

        /* Animated background */
        .bg-pattern {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            background: 
                radial-gradient(ellipse at 20% 20%, rgba(0, 255, 136, 0.05) 0%, transparent 50%),
                radial-gradient(ellipse at 80% 80%, rgba(255, 51, 102, 0.05) 0%, transparent 50%),
                radial-gradient(ellipse at 50% 50%, rgba(0, 170, 255, 0.03) 0%, transparent 70%);
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 2rem;
        }}

        /* Header */
        header {{
            text-align: center;
            padding: 3rem 0;
            position: relative;
        }}

        .logo {{
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 1rem;
            margin-bottom: 1rem;
        }}

        .logo-icon {{
            font-size: 3rem;
            animation: pulse 2s ease-in-out infinite;
        }}

        @keyframes pulse {{
            0%, 100% {{ transform: scale(1); }}
            50% {{ transform: scale(1.1); }}
        }}

        h1 {{
            font-size: clamp(2rem, 5vw, 3.5rem);
            font-weight: 700;
            background: linear-gradient(135deg, var(--text-primary) 0%, var(--accent-blue) 50%, var(--accent-purple) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 0.5rem;
        }}

        .subtitle {{
            color: var(--text-secondary);
            font-size: 1.1rem;
            font-weight: 300;
        }}

        .update-time {{
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            margin-top: 1rem;
            padding: 0.5rem 1rem;
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 100px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.85rem;
            color: var(--text-secondary);
        }}

        .live-dot {{
            width: 8px;
            height: 8px;
            background: var(--accent-green);
            border-radius: 50%;
            animation: blink 1.5s ease-in-out infinite;
        }}

        @keyframes blink {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.3; }}
        }}

        /* Tabs */
        .tabs {{
            margin-top: 1.25rem;
            display: flex;
            justify-content: center;
        }}

        .tab-group {{
            display: inline-flex;
            gap: 0.25rem;
            padding: 0.25rem;
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 999px;
        }}

        .tab-btn {{
            padding: 0.65rem 1.1rem;
            border-radius: 999px;
            background: transparent;
            border: 1px solid transparent;
            color: var(--text-secondary);
            font-family: 'Outfit', sans-serif;
            font-size: 0.95rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
        }}

        .tab-btn:hover {{
            background: var(--bg-hover);
            color: var(--text-primary);
        }}

        .tab-btn.active {{
            background: linear-gradient(135deg, var(--accent-blue), var(--accent-purple));
            color: var(--text-primary);
            box-shadow: 0 8px 30px rgba(0, 170, 255, 0.2);
        }}

        .hidden {{
            display: none !important;
        }}

        /* Market Summary */
        .market-summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin: 2rem 0;
        }}

        .summary-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 1.5rem;
            text-align: center;
            transition: all 0.3s ease;
        }}

        .summary-card:hover {{
            transform: translateY(-2px);
            border-color: var(--accent-blue);
        }}

        .summary-card.gainers {{
            border-top: 3px solid var(--accent-green);
        }}

        .summary-card.losers {{
            border-top: 3px solid var(--accent-red);
        }}

        .summary-card.neutral {{
            border-top: 3px solid var(--accent-blue);
        }}

        .summary-value {{
            font-size: 2.5rem;
            font-weight: 700;
            font-family: 'JetBrains Mono', monospace;
        }}

        .summary-card.gainers .summary-value {{
            color: var(--accent-green);
        }}

        .summary-card.losers .summary-value {{
            color: var(--accent-red);
        }}

        .summary-card.neutral .summary-value {{
            color: var(--accent-blue);
        }}

        .summary-label {{
            color: var(--text-secondary);
            font-size: 0.9rem;
            margin-top: 0.5rem;
        }}

        /* Download Section */
        .download-section {{
            display: flex;
            flex-wrap: wrap;
            gap: 1rem;
            justify-content: center;
            margin: 2rem 0;
        }}

        .download-btn {{
            display: inline-flex;
            align-items: center;
            gap: 0.75rem;
            padding: 0.875rem 1.5rem;
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            color: var(--text-primary);
            font-family: 'Outfit', sans-serif;
            font-size: 0.95rem;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.3s ease;
            text-decoration: none;
        }}

        .download-btn:hover {{
            background: var(--bg-hover);
            border-color: var(--accent-blue);
            transform: translateY(-2px);
        }}

        .download-btn.primary {{
            background: linear-gradient(135deg, var(--accent-blue), var(--accent-purple));
            border: none;
        }}

        .download-btn.primary:hover {{
            box-shadow: 0 8px 30px rgba(0, 170, 255, 0.3);
        }}

        .download-btn svg {{
            width: 20px;
            height: 20px;
        }}

        /* Tables Section */
        .tables-container {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(min(100%, 600px), 1fr));
            gap: 2rem;
            margin-top: 2rem;
        }}

        .table-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 20px;
            overflow: hidden;
        }}

        .table-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 1.5rem;
            border-bottom: 1px solid var(--border-color);
        }}

        .table-title {{
            display: flex;
            align-items: center;
            gap: 0.75rem;
            font-size: 1.25rem;
            font-weight: 600;
        }}

        .table-title.gainers {{
            color: var(--accent-green);
        }}

        .table-title.losers {{
            color: var(--accent-red);
        }}

        .table-icon {{
            font-size: 1.5rem;
        }}

        .table-wrapper {{
            overflow-x: auto;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.9rem;
        }}

        th {{
            background: var(--bg-secondary);
            color: var(--text-secondary);
            font-weight: 500;
            text-transform: uppercase;
            font-size: 0.75rem;
            letter-spacing: 0.05em;
            padding: 1rem;
            text-align: left;
            position: sticky;
            top: 0;
        }}

        th:first-child {{
            text-align: center;
        }}

        td {{
            padding: 1rem;
            border-bottom: 1px solid var(--border-color);
            transition: background 0.2s ease;
        }}

        tr:hover td {{
            background: var(--bg-hover);
        }}

        tr:last-child td {{
            border-bottom: none;
        }}

        .clickable-row {{
            cursor: pointer;
        }}

        .clickable-row:focus-visible td {{
            background: var(--bg-hover);
            box-shadow: inset 0 0 0 1px rgba(0, 170, 255, 0.6);
        }}

        .rank {{
            text-align: center;
            color: var(--text-muted);
            font-weight: 500;
        }}

        .symbol {{
            font-weight: 600;
            color: var(--text-primary);
        }}

        .price {{
            color: var(--text-secondary);
        }}

        .change, .change-pct {{
            font-weight: 600;
        }}

        .positive {{
            color: var(--accent-green);
        }}

        .negative {{
            color: var(--accent-red);
        }}

        .volume {{
            color: var(--text-muted);
            font-size: 0.85rem;
        }}

        /* Search and Filter */
        .controls {{
            display: flex;
            flex-wrap: wrap;
            gap: 1rem;
            margin: 2rem 0;
            justify-content: center;
        }}

        .search-box {{
            position: relative;
            flex: 1;
            max-width: 400px;
        }}

        .search-box input {{
            width: 100%;
            padding: 1rem 1rem 1rem 3rem;
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            color: var(--text-primary);
            font-family: 'Outfit', sans-serif;
            font-size: 1rem;
            transition: all 0.3s ease;
        }}

        .search-box input:focus {{
            outline: none;
            border-color: var(--accent-blue);
            box-shadow: 0 0 0 3px rgba(0, 170, 255, 0.1);
        }}

        .search-box input::placeholder {{
            color: var(--text-muted);
        }}

        .search-box svg {{
            position: absolute;
            left: 1rem;
            top: 50%;
            transform: translateY(-50%);
            width: 20px;
            height: 20px;
            color: var(--text-muted);
        }}

        /* Chart Modal */
        .chart-modal {{
            position: fixed;
            inset: 0;
            background: rgba(10, 10, 15, 0.86);
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 1.5rem;
            z-index: 1000;
        }}

        .chart-panel {{
            width: min(960px, 100%);
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.45);
            overflow: hidden;
        }}

        .chart-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 1.25rem 1.5rem;
            border-bottom: 1px solid var(--border-color);
        }}

        .chart-title {{
            font-size: 1.25rem;
            font-weight: 600;
        }}

        .chart-subtitle {{
            color: var(--text-secondary);
            font-size: 0.9rem;
        }}

        .chart-close {{
            width: 36px;
            height: 36px;
            border-radius: 10px;
            border: 1px solid var(--border-color);
            background: var(--bg-secondary);
            color: var(--text-primary);
            cursor: pointer;
            transition: all 0.2s ease;
        }}

        .chart-close:hover {{
            border-color: var(--accent-blue);
            transform: translateY(-1px);
        }}

        .chart-controls {{
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
            padding: 1rem 1.5rem;
            background: var(--bg-secondary);
            border-bottom: 1px solid var(--border-color);
        }}

        .chart-tabs {{
            display: inline-flex;
            flex-wrap: wrap;
            gap: 0.3rem;
            padding: 0.25rem;
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 12px;
        }}

        .chart-tab {{
            padding: 0.4rem 0.7rem;
            border-radius: 8px;
            border: 1px solid transparent;
            background: transparent;
            color: var(--text-secondary);
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.8rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
        }}

        .chart-tab:hover {{
            color: var(--text-primary);
            background: var(--bg-hover);
        }}

        .chart-tab.active {{
            background: linear-gradient(135deg, var(--accent-blue), var(--accent-purple));
            color: var(--text-primary);
            box-shadow: 0 4px 15px rgba(0, 170, 255, 0.2);
        }}

        .chart-note {{
            color: var(--text-muted);
            font-size: 0.8rem;
        }}


        .chart-body {{
            position: relative;
            padding: 1rem 1.5rem 1.5rem;
        }}

        #chartContainer {{
            width: 100%;
            height: 360px;
        }}

        .chart-state {{
            position: absolute;
            inset: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            background: rgba(10, 10, 15, 0.6);
            color: var(--text-secondary);
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.95rem;
            z-index: 2;
        }}

        /* Footer */
        footer {{
            text-align: center;
            padding: 3rem 0;
            margin-top: 3rem;
            border-top: 1px solid var(--border-color);
            color: var(--text-muted);
            font-size: 0.9rem;
        }}

        footer a {{
            color: var(--accent-blue);
            text-decoration: none;
        }}

        footer a:hover {{
            text-decoration: underline;
        }}

        /* Responsive */
        @media (max-width: 768px) {{
            .container {{
                padding: 1rem;
            }}

            header {{
                padding: 2rem 0;
            }}

            .market-summary {{
                grid-template-columns: repeat(2, 1fr);
            }}

            .table-header {{
                flex-direction: column;
                gap: 1rem;
                text-align: center;
            }}

            table {{
                font-size: 0.8rem;
            }}

            th, td {{
                padding: 0.75rem 0.5rem;
            }}

            .download-section {{
                flex-direction: column;
                align-items: stretch;
            }}

            .chart-controls {{
                flex-direction: column;
                align-items: flex-start;
            }}

            #chartContainer {{
                height: 280px;
            }}
        }}

        /* Animations */
        .fade-in {{
            animation: fadeIn 0.6s ease-out forwards;
            opacity: 0;
        }}

        @keyframes fadeIn {{
            to {{ opacity: 1; }}
        }}

        .slide-up {{
            animation: slideUp 0.6s ease-out forwards;
            opacity: 0;
            transform: translateY(20px);
        }}

        @keyframes slideUp {{
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}

        .delay-1 {{ animation-delay: 0.1s; }}
        .delay-2 {{ animation-delay: 0.2s; }}
        .delay-3 {{ animation-delay: 0.3s; }}
        .delay-4 {{ animation-delay: 0.4s; }}
    </style>
</head>
<body>
    <div class="bg-pattern"></div>
    
    <div class="container">
        <header class="fade-in">
            <div class="logo">
                <span class="logo-icon">📈</span>
            </div>
            <h1>S&P 500 Market Movers</h1>
            <p class="subtitle" id="subtitle">{daily_subtitle}</p>
            <div class="update-time">
                <span class="live-dot"></span>
                <span id="updateText">{daily_update_label}</span>
            </div>
            <div class="tabs">
                <div class="tab-group">
                    <button id="dailyTab" class="tab-btn active" onclick="switchView('daily')">Daily</button>
                    <button id="weeklyTab" class="tab-btn" onclick="switchView('weekly')">Weekly (Mon-Fri)</button>
                </div>
            </div>
        </header>

        <section class="market-summary slide-up delay-1" id="dailySummary">
            <div class="summary-card gainers">
                <div class="summary-value">{daily_total_gainers}</div>
                <div class="summary-label">Stocks Up</div>
            </div>
            <div class="summary-card losers">
                <div class="summary-value">{daily_total_losers}</div>
                <div class="summary-label">Stocks Down</div>
            </div>
            <div class="summary-card neutral">
                <div class="summary-value">{daily_total_unchanged}</div>
                <div class="summary-label">Unchanged</div>
            </div>
            <div class="summary-card {daily_avg_class}">
                <div class="summary-value">{daily_avg_change:+.2f}%</div>
                <div class="summary-label">Avg Change</div>
            </div>
        </section>

        <section class="market-summary slide-up delay-1 hidden" id="weeklySummary">
            <div class="summary-card gainers">
                <div class="summary-value">{weekly_total_gainers}</div>
                <div class="summary-label">Stocks Up</div>
            </div>
            <div class="summary-card losers">
                <div class="summary-value">{weekly_total_losers}</div>
                <div class="summary-label">Stocks Down</div>
            </div>
            <div class="summary-card neutral">
                <div class="summary-value">{weekly_total_unchanged}</div>
                <div class="summary-label">Unchanged</div>
            </div>
            <div class="summary-card {weekly_avg_class}">
                <div class="summary-value">{weekly_avg_change:+.2f}%</div>
                <div class="summary-label">Avg Change</div>
            </div>
        </section>

        <section class="controls slide-up delay-2">
            <div class="search-box">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
                <input type="text" id="searchInput" placeholder="Search by symbol (e.g., AAPL, MSFT)..." oninput="filterTables()">
            </div>
        </section>

        <section class="download-section slide-up delay-2" id="dailyDownloads">
            <a href="data/daily/gainers.csv" download class="download-btn primary">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                </svg>
                Download Gainers (CSV)
            </a>
            <a href="data/daily/losers.csv" download class="download-btn primary">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                </svg>
                Download Losers (CSV)
            </a>
            <a href="data/daily/all_stocks.csv" download class="download-btn">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                Download All S&P 500 (CSV)
            </a>
            <button onclick="copyTableData(event, 'daily')" class="download-btn">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                </svg>
                Copy to Clipboard
            </button>
        </section>

        <section class="download-section slide-up delay-2 hidden" id="weeklyDownloads">
            <a href="data/weekly/gainers.csv" download class="download-btn primary">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                </svg>
                Download Weekly Gainers (CSV)
            </a>
            <a href="data/weekly/losers.csv" download class="download-btn primary">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                </svg>
                Download Weekly Losers (CSV)
            </a>
            <a href="data/weekly/all_stocks.csv" download class="download-btn">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                Download Weekly All S&P 500 (CSV)
            </a>
            <button onclick="copyTableData(event, 'weekly')" class="download-btn">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                </svg>
                Copy to Clipboard
            </button>
        </section>

        <div class="tables-container" id="dailyTables">
            <div class="table-card slide-up delay-3">
                <div class="table-header">
                    <h2 class="table-title gainers">
                        <span class="table-icon">🟢</span>
                        Top 20 Gainers
                    </h2>
                </div>
                <div class="table-wrapper">
                    <table id="dailyGainersTable">
                        <thead>
                            <tr>
                                <th>#</th>
                                <th>Symbol</th>
                                <th>Price</th>
                                <th>Change</th>
                                <th>Change %</th>
                                <th>Volume</th>
                            </tr>
                        </thead>
                        <tbody>
                            {daily_gainers_rows}
                        </tbody>
                    </table>
                </div>
            </div>

            <div class="table-card slide-up delay-4">
                <div class="table-header">
                    <h2 class="table-title losers">
                        <span class="table-icon">🔴</span>
                        Top 20 Losers
                    </h2>
                </div>
                <div class="table-wrapper">
                    <table id="dailyLosersTable">
                        <thead>
                            <tr>
                                <th>#</th>
                                <th>Symbol</th>
                                <th>Price</th>
                                <th>Change</th>
                                <th>Change %</th>
                                <th>Volume</th>
                            </tr>
                        </thead>
                        <tbody>
                            {daily_losers_rows}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <div class="tables-container hidden" id="weeklyTables">
            <div class="table-card slide-up delay-3">
                <div class="table-header">
                    <h2 class="table-title gainers">
                        <span class="table-icon">🟢</span>
                        Top 20 Weekly Gainers
                    </h2>
                </div>
                <div class="table-wrapper">
                    <table id="weeklyGainersTable">
                        <thead>
                            <tr>
                                <th>#</th>
                                <th>Symbol</th>
                                <th>Week Start</th>
                                <th>Week End</th>
                                <th>Change</th>
                                <th>Change %</th>
                                <th>Avg Volume</th>
                            </tr>
                        </thead>
                        <tbody>
                            {weekly_gainers_rows}
                        </tbody>
                    </table>
                </div>
            </div>

            <div class="table-card slide-up delay-4">
                <div class="table-header">
                    <h2 class="table-title losers">
                        <span class="table-icon">🔴</span>
                        Top 20 Weekly Losers
                    </h2>
                </div>
                <div class="table-wrapper">
                    <table id="weeklyLosersTable">
                        <thead>
                            <tr>
                                <th>#</th>
                                <th>Symbol</th>
                                <th>Week Start</th>
                                <th>Week End</th>
                                <th>Change</th>
                                <th>Change %</th>
                                <th>Avg Volume</th>
                            </tr>
                        </thead>
                        <tbody>
                            {weekly_losers_rows}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <footer>
            <p>Data source: Yahoo Finance | S&P 500 Index</p>
            <p style="margin-top: 0.5rem;">Auto-updated after market close (Mon–Fri) + weekly refresh (Sat)</p>
            <p style="margin-top: 1rem;">
                <a href="https://github.com/Adarsh1999/market-movers" target="_blank">View on GitHub</a>
            </p>
        </footer>
    </div>

    <div class="chart-modal hidden" id="chartModal">
        <div class="chart-panel">
            <div class="chart-header">
                <div>
                    <div class="chart-title" id="chartTitle">Chart</div>
                    <div class="chart-subtitle" id="chartSubtitle">Candlestick view</div>
                </div>
                <button class="chart-close" id="chartClose" aria-label="Close chart">X</button>
            </div>
            <div class="chart-controls">
                <div class="chart-tabs">
                    <button class="chart-tab" data-range="m15">15M</button>
                    <button class="chart-tab" data-range="h1">1H</button>
                    <button class="chart-tab" data-range="h2">2H</button>
                    <button class="chart-tab" data-range="h3">3H</button>
                    <button class="chart-tab active" data-range="day">1D</button>
                    <button class="chart-tab" data-range="week">1W</button>
                    <button class="chart-tab" data-range="month">1M</button>
                </div>
                <div class="chart-note">Intraday (15M-3H) • Daily • Weekly • Monthly candlestick views</div>
            </div>

            <div class="chart-body">
                <div id="chartContainer"></div>
                <div class="chart-state hidden" id="chartState">Loading chart...</div>
            </div>
        </div>
    </div>

    <script src="https://unpkg.com/lightweight-charts@3.8.0/dist/lightweight-charts.standalone.production.js"></script>
    <script>
        // Store data for filtering and export
        const dailyAllStocks = {daily_all_stocks_json};
        const dailyGainers = {daily_gainers_json};
        const dailyLosers = {daily_losers_json};

        const weeklyAllStocks = {weekly_all_stocks_json};
        const weeklyGainers = {weekly_gainers_json};
        const weeklyLosers = {weekly_losers_json};

        const DAILY_SUBTITLE = "{daily_subtitle}";
        const WEEKLY_SUBTITLE = "{weekly_subtitle}";
        const DAILY_UPDATE_TEXT = "{daily_update_label}";
        const WEEKLY_UPDATE_TEXT = "{weekly_update_label}";
        const DEFAULT_VIEW = "{default_view}";
        const chartCache = {{}};

        const chartModal = document.getElementById('chartModal');
        const chartTitle = document.getElementById('chartTitle');
        const chartSubtitle = document.getElementById('chartSubtitle');
        const chartState = document.getElementById('chartState');
        const chartContainer = document.getElementById('chartContainer');
        const chartTabs = Array.from(document.querySelectorAll('.chart-tab'));
        const chartClose = document.getElementById('chartClose');

        let chartInstance = null;
        let candleSeries = null;
        let activeChartTicker = null;
        let activeChartRange = 'day';

        function switchView(view) {{
            const isWeekly = view === 'weekly';

            document.getElementById('dailySummary').classList.toggle('hidden', isWeekly);
            document.getElementById('weeklySummary').classList.toggle('hidden', !isWeekly);
            document.getElementById('dailyDownloads').classList.toggle('hidden', isWeekly);
            document.getElementById('weeklyDownloads').classList.toggle('hidden', !isWeekly);
            document.getElementById('dailyTables').classList.toggle('hidden', isWeekly);
            document.getElementById('weeklyTables').classList.toggle('hidden', !isWeekly);

            document.getElementById('dailyTab').classList.toggle('active', !isWeekly);
            document.getElementById('weeklyTab').classList.toggle('active', isWeekly);

            document.getElementById('subtitle').textContent = isWeekly ? WEEKLY_SUBTITLE : DAILY_SUBTITLE;
            document.getElementById('updateText').textContent = isWeekly ? WEEKLY_UPDATE_TEXT : DAILY_UPDATE_TEXT;

            filterTables();
        }}

        function setChartState(message) {{
            chartState.textContent = message;
            chartState.classList.remove('hidden');
        }}

        function clearChartState() {{
            chartState.classList.add('hidden');
        }}

        function ensureChart() {{
            if (typeof LightweightCharts === 'undefined') {{
                setChartState('Chart library unavailable.');
                return false;
            }}

            try {{
                if (!chartInstance) {{
                    // Use fallback dimensions if container not yet laid out
                    const width = chartContainer.clientWidth || 800;
                    const height = chartContainer.clientHeight || 360;

                    chartInstance = LightweightCharts.createChart(chartContainer, {{
                        layout: {{
                            background: {{ type: 'solid', color: 'transparent' }},
                            textColor: '#cfd3dc',
                            fontFamily: 'JetBrains Mono, monospace',
                        }},
                        grid: {{
                            vertLines: {{ color: 'rgba(255, 255, 255, 0.06)' }},
                            horzLines: {{ color: 'rgba(255, 255, 255, 0.06)' }},
                        }},
                        rightPriceScale: {{ borderVisible: false }},
                        timeScale: {{ borderVisible: false }},
                        width: width,
                        height: height,
                    }});

                    candleSeries = chartInstance.addCandlestickSeries({{
                        upColor: '#00ff88',
                        downColor: '#ff3366',
                        borderUpColor: '#00cc6a',
                        borderDownColor: '#cc2952',
                        wickUpColor: '#00cc6a',
                        wickDownColor: '#cc2952',
                    }});
                }} else {{
                    // Update dimensions for existing chart
                    const width = chartContainer.clientWidth || 800;
                    const height = chartContainer.clientHeight || 360;
                    chartInstance.applyOptions({{ width: width, height: height }});
                }}

                return true;
            }} catch (e) {{
                console.error('Chart creation error:', e);
                setChartState('Chart initialization failed.');
                return false;
            }}
        }}

        function normalizeChartData(series) {{
            const sanitized = [];
            series.forEach(bar => {{
                if (!bar) {{
                    return;
                }}

                let timeValue = bar.time;
                if (typeof timeValue === 'string') {{
                    const parts = timeValue.split('-').map(Number);
                    timeValue = Date.UTC(parts[0], parts[1] - 1, parts[2]) / 1000;
                }}

                const open = Number(bar.open);
                const high = Number(bar.high);
                const low = Number(bar.low);
                const close = Number(bar.close);

                if (!Number.isFinite(timeValue) || !Number.isFinite(open) || !Number.isFinite(high) || !Number.isFinite(low) || !Number.isFinite(close)) {{
                    return;
                }}

                const maxBody = Math.max(open, close);
                const minBody = Math.min(open, close);
                const fixedHigh = Math.max(high, maxBody);
                const fixedLow = Math.min(low, minBody);

                sanitized.push({{
                    time: timeValue,
                    open,
                    high: fixedHigh,
                    low: fixedLow,
                    close,
                }});
            }});

            sanitized.sort((a, b) => a.time - b.time);
            const deduped = [];
            let lastTime = null;
            sanitized.forEach(bar => {{
                if (bar.time === lastTime) {{
                    deduped[deduped.length - 1] = bar;
                    return;
                }}
                deduped.push(bar);
                lastTime = bar.time;
            }});

            return deduped;
        }}

        function renderChartData(payload, range) {{
            if (!candleSeries || !chartInstance) {{
                console.error('Chart not initialized');
                setChartState('Chart not initialized.');
                return;
            }}

            const series = payload && payload[range] ? payload[range] : [];
            console.log(`Rendering ${{range}} data: ${{series.length}} candles`);

            if (!series.length) {{
                setChartState('No ' + range + ' data available.');
                candleSeries.setData([]);
                return;
            }}

            clearChartState();
            const normalized = normalizeChartData(series);
            console.log(`Normalized data: ${{normalized.length}} candles`);

            if (!normalized.length) {{
                setChartState('No valid chart data after normalization.');
                candleSeries.setData([]);
                return;
            }}

            candleSeries.setData(normalized);
            chartInstance.timeScale().fitContent();
        }}

        function loadChartData(ticker) {{
            if (chartCache[ticker]) {{
                return Promise.resolve(chartCache[ticker]);
            }}

            setChartState('Loading chart data...');
            return fetch(`data/charts/${{encodeURIComponent(ticker)}}.json`)
                .then(response => {{
                    if (!response.ok) {{
                        throw new Error('Chart not found');
                    }}
                    return response.json();
                }})
                .then(payload => {{
                    chartCache[ticker] = payload;
                    return payload;
                }});
        }}

        function getTimeframeLabel(range) {{
            const labels = {{
                'm15': '15-Minute Candles',
                'h1': '1-Hour Candles',
                'h2': '2-Hour Candles',
                'h3': '3-Hour Candles',
                'day': 'Daily Candles',
                'week': 'Weekly Candles',
                'month': 'Monthly Candles'
            }};
            return labels[range] || 'Candlestick Chart';
        }}

        function setActiveChartRange(range) {{
            activeChartRange = range;
            chartTabs.forEach(tab => {{
                tab.classList.toggle('active', tab.dataset.range === range);
            }});

            // Update subtitle based on selected timeframe
            chartSubtitle.textContent = getTimeframeLabel(range);

            if (activeChartTicker && chartCache[activeChartTicker]) {{
                renderChartData(chartCache[activeChartTicker], activeChartRange);
            }}
        }}


        function openChart(ticker) {{
            activeChartTicker = ticker;
            chartTitle.textContent = `${{ticker}} Candlesticks`;
            chartSubtitle.textContent = getTimeframeLabel(activeChartRange);
            chartModal.classList.remove('hidden');
            setChartState('Loading chart...');


            // Use requestAnimationFrame to ensure DOM is laid out before creating chart
            requestAnimationFrame(() => {{
                if (!ensureChart()) {{
                    return;
                }}
                setActiveChartRange(activeChartRange);
                loadChartData(ticker)
                    .then(payload => {{
                        try {{
                            renderChartData(payload, activeChartRange);
                        }} catch (renderErr) {{
                            console.error('Chart render error:', renderErr);
                            setChartState('Chart render failed: ' + renderErr.message);
                        }}
                    }})
                    .catch(error => {{
                        console.error('Chart load error:', error);
                        setChartState('Chart data unavailable: ' + error.message);
                    }});
            }});
        }}

        function closeChart() {{
            chartModal.classList.add('hidden');
        }}

        function bindChartRows() {{
            const rows = document.querySelectorAll('.clickable-row');
            rows.forEach(row => {{
                const ticker = row.dataset.ticker;
                if (!ticker) {{
                    return;
                }}
                row.addEventListener('click', () => openChart(ticker));
                row.addEventListener('keydown', event => {{
                    if (event.key === 'Enter' || event.key === ' ') {{
                        event.preventDefault();
                        openChart(ticker);
                    }}
                }});
            }});
        }}

        function filterTables() {{
            const searchTerm = document.getElementById('searchInput').value.toUpperCase();
            const tableIds = ['dailyGainersTable', 'dailyLosersTable', 'weeklyGainersTable', 'weeklyLosersTable'];

            tableIds.forEach(id => {{
                const rows = document.querySelectorAll('#' + id + ' tbody tr');
                rows.forEach(row => {{
                    const symbolEl = row.querySelector('.symbol');
                    const symbol = symbolEl ? symbolEl.textContent.toUpperCase() : '';
                    row.style.display = symbol.includes(searchTerm) ? '' : 'none';
                }});
            }});
        }}

        function copyTableData(evt, view) {{
            const isWeekly = view === 'weekly';
            const gainers = isWeekly ? weeklyGainers : dailyGainers;
            const losers = isWeekly ? weeklyLosers : dailyLosers;
            const updateText = isWeekly ? WEEKLY_UPDATE_TEXT : DAILY_UPDATE_TEXT;

            let text = 'S&P 500 Market Movers - ' + (isWeekly ? 'WEEKLY (MON-FRI)' : 'DAILY') + '\\n';
            text += updateText + '\\n\\n';

            if (!isWeekly) {{
                text += 'TOP GAINERS\\n';
                text += 'Symbol\\tPrice\\tChange\\tChange%\\tVolume\\n';
                gainers.forEach(s => {{
                    text += s.ticker + '\\t$' + s.price + '\\t' + (s.change >= 0 ? '+' : '') + '$' + s.change + '\\t' + (s.change_pct >= 0 ? '+' : '') + s.change_pct + '%\\t' + (s.volume || 0).toLocaleString() + '\\n';
                }});

                text += '\\nTOP LOSERS\\n';
                text += 'Symbol\\tPrice\\tChange\\tChange%\\tVolume\\n';
                losers.forEach(s => {{
                    text += s.ticker + '\\t$' + s.price + '\\t$' + s.change + '\\t' + s.change_pct + '%\\t' + (s.volume || 0).toLocaleString() + '\\n';
                }});
            }} else {{
                text += 'TOP WEEKLY GAINERS\\n';
                text += 'Symbol\\tWeekStart\\tWeekEnd\\tChange\\tChange%\\tAvgVol\\n';
                gainers.forEach(s => {{
                    text += s.ticker + '\\t$' + s.start_price + '\\t$' + s.end_price + '\\t' + (s.change >= 0 ? '+' : '') + '$' + s.change + '\\t' + (s.change_pct >= 0 ? '+' : '') + s.change_pct + '%\\t' + (s.avg_volume || 0).toLocaleString() + '\\n';
                }});

                text += '\\nTOP WEEKLY LOSERS\\n';
                text += 'Symbol\\tWeekStart\\tWeekEnd\\tChange\\tChange%\\tAvgVol\\n';
                losers.forEach(s => {{
                    text += s.ticker + '\\t$' + s.start_price + '\\t$' + s.end_price + '\\t$' + s.change + '\\t' + s.change_pct + '%\\t' + (s.avg_volume || 0).toLocaleString() + '\\n';
                }});
            }}

            navigator.clipboard.writeText(text).then(() => {{
                const btn = evt.currentTarget;
                const originalText = btn.innerHTML;
                btn.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" style="width:20px;height:20px"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" /></svg> Copied!';
                setTimeout(() => {{ btn.innerHTML = originalText; }}, 2000);
            }});
        }}

        // Default view: daily on weekdays, weekly on weekends (when available)
        document.addEventListener('DOMContentLoaded', () => {{
            switchView(DEFAULT_VIEW === 'weekly' ? 'weekly' : 'daily');
            bindChartRows();
        }});

        chartTabs.forEach(tab => {{
            tab.addEventListener('click', () => {{
                setActiveChartRange(tab.dataset.range);
            }});
        }});

        chartClose.addEventListener('click', closeChart);

        chartModal.addEventListener('click', event => {{
            if (event.target === chartModal) {{
                closeChart();
            }}
        }});

        document.addEventListener('keydown', event => {{
            if (event.key === 'Escape' && !chartModal.classList.contains('hidden')) {{
                closeChart();
            }}
        }});

        window.addEventListener('resize', () => {{
            if (chartInstance) {{
                chartInstance.applyOptions({{
                    width: chartContainer.clientWidth,
                    height: chartContainer.clientHeight,
                }});
            }}
        }});
    </script>
</body>
</html>'''
    
    return html


def main():
    """Main function to generate the static site"""
    print("=" * 60)
    print("🚀 S&P 500 Market Movers - Static Site Generator")
    print("=" * 60)
    
    # Create output directory
    os.makedirs('dist', exist_ok=True)
    os.makedirs('dist/data', exist_ok=True)
    os.makedirs('dist/data/daily', exist_ok=True)
    os.makedirs('dist/data/weekly', exist_ok=True)
    os.makedirs('dist/data/charts', exist_ok=True)

    # Use US/Eastern for display (market context)
    eastern = ZoneInfo("America/New_York")
    generated_at_et = datetime.now(timezone.utc).astimezone(eastern)
    
    # Download data once (enough for weekly + daily)
    print("\n📊 Downloading S&P 500 market data...")
    data = download_sp500_history(period="10d")

    # Build DAILY dataset
    print("\n📅 Building DAILY dataset...")
    daily_all_stocks, daily_meta = build_daily_dataset(data)
    if not daily_all_stocks:
        raise ValueError("No DAILY stock data retrieved")

    daily_gainers, daily_losers = get_top_movers(daily_all_stocks, limit=20)
    daily_sorted_all = sorted(daily_all_stocks, key=lambda x: x["change_pct"], reverse=True)
    print(f"   Daily: {len(daily_gainers)} gainers, {len(daily_losers)} losers")

    # Build WEEKLY dataset (completed Mon-Fri range)
    weekly_start_date, weekly_end_date = get_week_date_range(generated_at_et)
    print(f"\n🗓️  Building WEEKLY (Mon-Fri) dataset... ({weekly_start_date} to {weekly_end_date})")
    weekly_all_stocks, weekly_meta = build_weekly_dataset(
        data,
        start_date=weekly_start_date,
        end_date=weekly_end_date,
    )
    weekly_gainers, weekly_losers = get_top_movers(weekly_all_stocks, limit=20) if weekly_all_stocks else ([], [])
    weekly_sorted_all = (
        sorted(weekly_all_stocks, key=lambda x: x["change_pct"], reverse=True) if weekly_all_stocks else []
    )
    print(f"   Weekly: {len(weekly_gainers)} gainers, {len(weekly_losers)} losers")

    # Build chart data for top movers
    chart_tickers = sorted(
        {
            stock["ticker"]
            for stock in (daily_gainers + daily_losers + weekly_gainers + weekly_losers)
        }
    )
    
    # Download daily chart history
    chart_history = download_chart_history(chart_tickers, period=CHART_PERIOD)
    
    # Download intraday data for charts
    print("\n📈 Downloading intraday chart data...")
    intraday_15m = download_intraday_15m(chart_tickers)
    intraday_1h = download_intraday_1h(chart_tickers)
    
    # Build chart payloads with all timeframes
    chart_payloads = build_chart_payloads(
        chart_history, 
        chart_tickers, 
        data_15m=intraday_15m, 
        data_1h=intraday_1h
    )
    write_chart_payloads(chart_payloads, "dist/data/charts")
    print(f"   Charts: {len(chart_payloads)} tickers (with intraday data)")


    # Generate CSV files
    print("\n📁 Generating CSV files...")
    generate_daily_csv(daily_gainers, "dist/data/daily/gainers.csv")
    generate_daily_csv(daily_losers, "dist/data/daily/losers.csv")
    generate_daily_csv(daily_sorted_all, "dist/data/daily/all_stocks.csv")

    generate_weekly_csv(weekly_gainers, "dist/data/weekly/gainers.csv")
    generate_weekly_csv(weekly_losers, "dist/data/weekly/losers.csv")
    generate_weekly_csv(weekly_sorted_all, "dist/data/weekly/all_stocks.csv")

    # Generate HTML
    print("\n🎨 Generating HTML page...")
    html = generate_html(
        daily_gainers,
        daily_losers,
        daily_all_stocks,
        daily_meta,
        weekly_gainers,
        weekly_losers,
        weekly_all_stocks,
        weekly_meta,
        generated_at_et,
    )
    
    with open('dist/index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("   Generated dist/index.html")
    
    # Save JSON data for API-like access
    print("\n💾 Generating JSON data...")
    with open('dist/data/data.json', 'w') as f:
        json.dump(
            {
                "generated_at": generated_at_et.isoformat(),
                "timezone": "America/New_York",
                "daily": {
                    "meta": daily_meta,
                    "gainers": daily_gainers,
                    "losers": daily_losers,
                    "all_stocks": daily_sorted_all,
                },
                "weekly": {
                    "meta": weekly_meta,
                    "gainers": weekly_gainers,
                    "losers": weekly_losers,
                    "all_stocks": weekly_sorted_all,
                },
            },
            f,
            indent=2,
        )
    print("   Generated dist/data/data.json")
    
    print("\n" + "=" * 60)
    print("✅ Site generated successfully!")
    print(f"   📁 Output: dist/")
    print(f"   📄 index.html - Main page")
    print(f"   📊 data/daily/gainers.csv - Daily top gainers")
    print(f"   📊 data/daily/losers.csv - Daily top losers")
    print(f"   📊 data/daily/all_stocks.csv - All S&P 500 (daily)")
    print(f"   📊 data/weekly/gainers.csv - Weekly top gainers")
    print(f"   📊 data/weekly/losers.csv - Weekly top losers")
    print(f"   📊 data/weekly/all_stocks.csv - All S&P 500 (weekly)")
    print(f"   📊 data/data.json - JSON API")
    print("=" * 60)


if __name__ == "__main__":
    main()
