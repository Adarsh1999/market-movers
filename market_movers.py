import os
import requests
import yfinance as yf
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- CONFIG ---
RESEND_API_KEY = os.environ.get("RESEND_API_KEY")
EMAIL_FROM = os.environ.get("EMAIL_FROM", "Market Movers <onboarding@resend.dev>")

# Support multiple emails (comma-separated)
email_to_str = os.environ.get("EMAIL_TO", "")
EMAIL_TO = [email.strip() for email in email_to_str.split(",") if email.strip()]

RESEND_URL = "https://api.resend.com/emails"

# S&P 500 tickers (comprehensive list)
SP500_TICKERS = [
    'MMM', 'AOS', 'ABT', 'ABBV', 'ACN', 'ADM', 'ADBE', 'ADP', 'AES', 'AFL',
    'A', 'APD', 'AKAM', 'ALB', 'ARE', 'ALGN', 'ALLE', 'LNT', 'ALL', 'GOOGL',
    'GOOG', 'MO', 'AMZN', 'AMCR', 'AMD', 'AEE', 'AAL', 'AEP', 'AXP', 'AIG',
    'AMT', 'AWK', 'AMP', 'AME', 'AMGN', 'APH', 'ADI', 'AON', 'APA',
    'AAPL', 'AMAT', 'APTV', 'ANET', 'AJG', 'AIZ', 'T', 'ATO', 'ADSK', 'AZO',
    'AVB', 'AVY', 'AXON', 'BKR', 'BALL', 'BAC', 'BBWI', 'BAX', 'BDX', 'BRK-B',
    'BBY', 'BIO', 'TECH', 'BIIB', 'BLK', 'BK', 'BA', 'BKNG', 'BWA', 'BSX',
    'BMY', 'AVGO', 'BR', 'BRO', 'BLDR', 'BG', 'CDNS', 'CZR', 'CPT', 'CPB',
    'COF', 'CAH', 'KMX', 'CCL', 'CARR', 'CAT', 'CBOE', 'CBRE', 'CDW', 'CE',
    'CNC', 'CNP', 'DAY', 'CF', 'CRL', 'SCHW', 'CHTR', 'CVX', 'CMG', 'CB',
    'CHD', 'CI', 'CINF', 'CTAS', 'CSCO', 'C', 'CFG', 'CLX', 'CME', 'CMS',
    'KO', 'CTSH', 'CL', 'CMCSA', 'CMA', 'CAG', 'COP', 'ED', 'STZ', 'CEG',
    'COO', 'CPRT', 'GLW', 'CTVA', 'CSGP', 'COST', 'CTRA', 'CCI', 'CSX', 'CMI',
    'CVS', 'DHI', 'DHR', 'DRI', 'DVA', 'DE', 'DAL', 'DXCM', 'FANG',
    'DLR', 'DG', 'DLTR', 'D', 'DPZ', 'DOV', 'DOW', 'DTE', 'DUK',
    'DD', 'EMN', 'ETN', 'EBAY', 'ECL', 'EIX', 'EW', 'EA', 'ELV', 'LLY',
    'EMR', 'ENPH', 'ENTG', 'EOG', 'EPAM', 'EQT', 'EFX', 'EQIX', 'EQR', 'ESS',
    'EL', 'ETSY', 'EG', 'EVRG', 'ES', 'EXC', 'EXPE', 'XOM',
    'FFIV', 'FDS', 'FICO', 'FAST', 'FRT', 'FDX', 'FITB',
    'FSLR', 'FE', 'FIS', 'FI', 'FMC', 'F', 'FTNT', 'FTV', 'FOXA', 'FOX', 'BEN', 'FCX',
    'GRMN', 'IT', 'GEHC', 'GEN', 'GNRC', 'GD', 'GE', 'GIS', 'GM', 'GPC',
    'GILD', 'GL', 'GPN', 'GS', 'HAL', 'HIG', 'HAS', 'HCA', 'HSIC', 'HSY',
    'HPE', 'HLT', 'HOLX', 'HD', 'HON', 'HRL', 'HST', 'HWM', 'HPQ', 'HUBB', 'HUM',
    'HBAN', 'HII', 'IBM', 'IEX', 'IDXX', 'ITW', 'ILMN', 'INCY', 'IR', 'PODD', 'INTC',
    'ICE', 'IFF', 'IP', 'IPG', 'INTU', 'ISRG', 'IVZ', 'INVH', 'IQV', 'IRM',
    'JBHT', 'JBL', 'JKHY', 'J', 'JNJ', 'JCI', 'JPM', 'K', 'KVUE', 'KDP', 'KEY',
    'KEYS', 'KMB', 'KIM', 'KMI', 'KLAC', 'KHC', 'KR', 'LHX', 'LH', 'LRCX',
    'LW', 'LVS', 'LDOS', 'LEN', 'LIN', 'LYV', 'LKQ', 'LMT', 'L', 'LOW',
    'LULU', 'LYB', 'MTB', 'MPC', 'MKTX', 'MAR', 'MMC', 'MLM', 'MAS', 'MA', 'MTCH', 'MKC', 'MCD', 'MCK', 'MDT', 'MRK',
    'META', 'MET', 'MTD', 'MGM', 'MCHP', 'MU', 'MSFT', 'MAA', 'MRNA', 'MHK',
    'MOH', 'TAP', 'MDLZ', 'MPWR', 'MNST', 'MCO', 'MS', 'MOS', 'MSI',
    'MSCI', 'NDAQ', 'NTAP', 'NFLX', 'NEM', 'NWSA', 'NWS', 'NEE', 'NKE', 'NI', 'NDSN',
    'NSC', 'NTRS', 'NOC', 'NCLH', 'NRG', 'NUE', 'NVDA', 'NVR', 'NXPI', 'ORLY', 'OXY',
    'ODFL', 'OMC', 'ON', 'OKE', 'ORCL', 'OTIS', 'PCAR', 'PKG', 'PANW', 'PH',
    'PAYX', 'PAYC', 'PYPL', 'PNR', 'PEP', 'PFE', 'PCG', 'PM', 'PSX', 'PNW',
    'PNC', 'POOL', 'PPG', 'PPL', 'PFG', 'PG', 'PGR', 'PLD', 'PRU',
    'PEG', 'PTC', 'PSA', 'PHM', 'QRVO', 'PWR', 'QCOM', 'DGX', 'RL', 'RJF',
    'RTX', 'O', 'REG', 'REGN', 'RF', 'RSG', 'RMD', 'RVTY', 'RHI', 'ROK',
    'ROL', 'ROP', 'ROST', 'RCL', 'SPGI', 'CRM', 'SBAC', 'SLB', 'STX', 'SRE',
    'NOW', 'SHW', 'SPG', 'SWKS', 'SJM', 'SNA', 'SO', 'LUV',
    'SWK', 'SBUX', 'STT', 'STLD', 'STE', 'SYK', 'SYF', 'SNPS', 'SYY',
    'TMUS', 'TROW', 'TTWO', 'TPR', 'TGT', 'TEL', 'TDY', 'TFX', 'TER', 'TSLA', 'TXN', 'TXT', 'TMO',
    'TJX', 'TSCO', 'TT', 'TDG', 'TRV', 'TRMB', 'TFC', 'TYL', 'TSN', 'USB',
    'UDR', 'ULTA', 'UNP', 'UAL', 'UPS', 'URI', 'UNH', 'UHS', 'VLO', 'VTR', 'VRSN', 'VRSK',
    'VZ', 'VRTX', 'VFC', 'VTRS', 'VICI', 'V', 'VMC', 'WAB', 'WMT', 'WBD', 'DIS',
    'WM', 'WAT', 'WEC', 'WFC', 'WELL', 'WST', 'WDC', 'WY', 'WHR', 'WMB', 'WTW', 'GWW',
    'WYNN', 'XEL', 'XYL', 'YUM', 'ZBRA', 'ZBH', 'ZION', 'ZTS', 'SOLV'
]


def is_weekend():
    """Check if today is Saturday (5) or Sunday (6)"""
    return datetime.now().weekday() in [5, 6]


def fetch_sp500_data(weekly=False):
    """Fetch stock data for all S&P 500 stocks using yfinance
    
    Args:
        weekly: If True, fetch 5 trading days of data for weekly summary
    """
    mode = "weekly" if weekly else "daily"
    print(f"Fetching {mode} data for {len(SP500_TICKERS)} S&P 500 stocks...")
    
    # Download data for all tickers at once (much faster)
    tickers_str = ' '.join(SP500_TICKERS)
    
    # For weekly data, we need at least 6 days to capture 5 trading days
    # (accounting for weekends and potential holidays)
    period = '7d' if weekly else '2d'
    
    # Suppress warnings and use auto_adjust=True
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        data = yf.download(tickers_str, period=period, progress=False, threads=True, auto_adjust=True, ignore_tz=True)
    
    results = []
    
    for ticker in SP500_TICKERS:
        try:
            # Get closing prices
            if len(SP500_TICKERS) > 1:
                close_prices = data['Close'][ticker]
            else:
                close_prices = data['Close']
            
            # Drop NaN values to get only trading days
            close_prices = close_prices.dropna()
            
            # Need at least 2 days of data
            if len(close_prices) < 2:
                continue
            
            if weekly:
                # For weekly: compare first day to last day of the week
                # Get up to 5 trading days
                trading_days = close_prices.tail(5)
                if len(trading_days) < 2:
                    continue
                    
                week_start_close = trading_days.iloc[0]
                week_end_close = trading_days.iloc[-1]
                
                # Skip if no valid data
                if week_start_close == 0 or week_end_close == 0:
                    continue
                
                # Calculate weekly change
                change = week_end_close - week_start_close
                change_pct = (change / week_start_close) * 100
                
                # Get average volume for the week
                if len(SP500_TICKERS) > 1:
                    volume_data = data['Volume'][ticker].dropna().tail(5)
                else:
                    volume_data = data['Volume'].dropna().tail(5)
                avg_volume = volume_data.mean() if len(volume_data) > 0 else 0
                
                # Get the number of trading days captured
                days_captured = len(trading_days)
                
                results.append({
                    'ticker': ticker,
                    'price': week_end_close,
                    'week_start_price': week_start_close,
                    'change': change,
                    'change_percentage': f"{change_pct:+.2f}%",
                    'change_pct_raw': change_pct,
                    'volume': int(avg_volume) if avg_volume > 0 else 0,
                    'days_captured': days_captured
                })
            else:
                # Daily mode: compare yesterday to today
                prev_close = close_prices.iloc[-2]
                current_close = close_prices.iloc[-1]
                
                # Skip if no valid data
                if prev_close == 0 or current_close == 0:
                    continue
                
                # Calculate change
                change = current_close - prev_close
                change_pct = (change / prev_close) * 100
                
                # Get volume
                if len(SP500_TICKERS) > 1:
                    volume = data['Volume'][ticker].iloc[-1]
                else:
                    volume = data['Volume'].iloc[-1]
                
                results.append({
                    'ticker': ticker,
                    'price': current_close,
                    'change': change,
                    'change_percentage': f"{change_pct:+.2f}%",
                    'change_pct_raw': change_pct,
                    'volume': int(volume) if volume > 0 else 0
                })
        except Exception as e:
            # Skip stocks with errors
            continue
    
    print(f"Successfully fetched {mode} data for {len(results)} stocks")
    return results


def get_top_movers(stocks, limit=20):
    """Get top gainers and losers from the stock list"""
    # Sort by percentage change
    sorted_stocks = sorted(stocks, key=lambda x: x['change_pct_raw'], reverse=True)
    
    # Top gainers (highest positive change)
    gainers = [s for s in sorted_stocks if s['change_pct_raw'] > 0][:limit]
    
    # Top losers (most negative change)
    losers = [s for s in sorted_stocks if s['change_pct_raw'] < 0][-limit:]
    losers.reverse()  # Most negative first
    
    return gainers, losers


def build_html_table(stocks, is_gainers=True, weekly=False):
    """Build an HTML table for the stock data"""
    color = "#22c55e" if is_gainers else "#ef4444"
    
    if weekly:
        title = "🟢 Top Weekly Gainers" if is_gainers else "🔴 Top Weekly Losers"
    else:
        title = "🟢 Top S&P 500 Gainers" if is_gainers else "🔴 Top S&P 500 Losers"
    
    if not stocks:
        return f"""
        <div style="margin-bottom: 30px;">
            <h2 style="color: #1f2937; margin-bottom: 10px;">{title}</h2>
            <p style="color: #6b7280;">No data available</p>
        </div>
        """
    
    rows = ""
    for i, stock in enumerate(stocks, 1):
        change_pct = stock["change_percentage"]
        volume = stock.get("volume", 0)
        
        if weekly:
            week_start = stock.get("week_start_price", stock["price"])
            rows += f"""
            <tr style="border-bottom: 1px solid #e5e7eb;">
                <td style="padding: 8px; text-align: center;">{i}</td>
                <td style="padding: 8px; font-weight: bold;">{stock["ticker"]}</td>
                <td style="padding: 8px; text-align: right;">${float(week_start):.2f}</td>
                <td style="padding: 8px; text-align: right;">${float(stock["price"]):.2f}</td>
                <td style="padding: 8px; text-align: right; color: {color}; font-weight: bold;">{change_pct}</td>
                <td style="padding: 8px; text-align: right;">{volume:,}</td>
            </tr>
            """
        else:
            rows += f"""
            <tr style="border-bottom: 1px solid #e5e7eb;">
                <td style="padding: 8px; text-align: center;">{i}</td>
                <td style="padding: 8px; font-weight: bold;">{stock["ticker"]}</td>
                <td style="padding: 8px; text-align: right;">${float(stock["price"]):.2f}</td>
                <td style="padding: 8px; text-align: right; color: {color};">{change_pct}</td>
                <td style="padding: 8px; text-align: right;">{volume:,}</td>
            </tr>
            """
    
    if weekly:
        header_row = """
                    <th style="padding: 10px; text-align: center; width: 50px;">#</th>
                    <th style="padding: 10px; text-align: left;">Symbol</th>
                    <th style="padding: 10px; text-align: right;">Week Start</th>
                    <th style="padding: 10px; text-align: right;">Week End</th>
                    <th style="padding: 10px; text-align: right;">Weekly Change</th>
                    <th style="padding: 10px; text-align: right;">Avg Volume</th>
        """
    else:
        header_row = """
                    <th style="padding: 10px; text-align: center; width: 50px;">#</th>
                    <th style="padding: 10px; text-align: left;">Symbol</th>
                    <th style="padding: 10px; text-align: right;">Price</th>
                    <th style="padding: 10px; text-align: right;">Change %</th>
                    <th style="padding: 10px; text-align: right;">Volume</th>
        """
    
    return f"""
    <div style="margin-bottom: 30px;">
        <h2 style="color: #1f2937; margin-bottom: 10px;">{title}</h2>
        <table style="width: 100%; border-collapse: collapse; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 14px;">
            <thead>
                <tr style="background-color: #f3f4f6;">
                    {header_row}
                </tr>
            </thead>
            <tbody>
                {rows}
            </tbody>
        </table>
    </div>
    """


def build_email_html(gainers, losers):
    """Build the complete email HTML for daily report"""
    today = datetime.now().strftime("%A, %B %d, %Y")
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    gainers_table = build_html_table(gainers, is_gainers=True)
    losers_table = build_html_table(losers, is_gainers=False)
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; background-color: #ffffff;">
        <div style="text-align: center; margin-bottom: 30px;">
            <h1 style="color: #1f2937; margin-bottom: 5px;">📈 S&P 500 Market Movers</h1>
            <p style="color: #6b7280; margin: 0;">{today}</p>
            <p style="color: #9ca3af; font-size: 12px; margin-top: 5px;">Generated: {now}</p>
        </div>
        
        {gainers_table}
        {losers_table}
        
        <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #e5e7eb; text-align: center; color: #9ca3af; font-size: 12px;">
            <p>Data source: Yahoo Finance | S&P 500 Index</p>
        </div>
    </body>
    </html>
    """


def build_weekly_email_html(gainers, losers):
    """Build the complete email HTML for weekly summary - top 20 gainers and losers"""
    today = datetime.now()
    # Calculate the week range (Monday to Friday of the past week)
    days_since_friday = (today.weekday() - 4) % 7
    if days_since_friday == 0:
        days_since_friday = 7 if today.weekday() > 4 else 0
    week_end = today - timedelta(days=days_since_friday)
    week_start = week_end - timedelta(days=4)
    
    week_range = f"{week_start.strftime('%b %d')} - {week_end.strftime('%b %d, %Y')}"
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    gainers_table = build_html_table(gainers, is_gainers=True, weekly=True)
    losers_table = build_html_table(losers, is_gainers=False, weekly=True)
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; background-color: #ffffff;">
        <div style="text-align: center; margin-bottom: 30px;">
            <h1 style="color: #1f2937; margin-bottom: 5px;">📊 Weekly S&P 500 Market Movers</h1>
            <p style="color: #6b7280; margin: 0;">{week_range}</p>
            <p style="color: #9ca3af; font-size: 12px; margin-top: 5px;">Cumulative 5-Day Performance | Generated: {now}</p>
        </div>
        
        {gainers_table}
        {losers_table}
        
        <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #e5e7eb; text-align: center; color: #9ca3af; font-size: 12px;">
            <p>Data source: Yahoo Finance | S&P 500 Index</p>
        </div>
    </body>
    </html>
    """


def send_email(html_content, weekly=False):
    """Send email via Resend API to multiple recipients"""
    today = datetime.now()
    
    if not EMAIL_TO:
        raise ValueError("EMAIL_TO is not set. Please set it in .env or GitHub Secrets.")
    
    if weekly:
        # Calculate the week range for subject
        days_since_friday = (today.weekday() - 4) % 7
        if days_since_friday == 0:
            days_since_friday = 7 if today.weekday() > 4 else 0
        week_end = today - timedelta(days=days_since_friday)
        week_start = week_end - timedelta(days=4)
        subject = f"📊 Weekly S&P 500 Summary - {week_start.strftime('%b %d')} to {week_end.strftime('%b %d')}"
    else:
        subject = f"📈 S&P 500 Market Movers - {today.strftime('%b %d, %Y')}"
    
    payload = {
        "from": EMAIL_FROM,
        "to": EMAIL_TO,  # List of emails
        "subject": subject,
        "html": html_content
    }
    
    headers = {
        "Authorization": f"Bearer {RESEND_API_KEY}",
        "Content-Type": "application/json"
    }
    
    print(f"Sending to {len(EMAIL_TO)} recipient(s): {', '.join(EMAIL_TO)}")
    response = requests.post(RESEND_URL, json=payload, headers=headers, timeout=30)
    response.raise_for_status()
    return response.json()


def main():
    # Check if we should run weekly summary (weekend) or daily report
    weekend = is_weekend()
    
    # Allow forcing weekly mode via environment variable for testing
    force_weekly = os.environ.get("FORCE_WEEKLY", "").lower() in ["true", "1", "yes"]
    weekly_mode = weekend or force_weekly
    
    if weekly_mode:
        print("=" * 50)
        print("🗓️  WEEKEND MODE: Generating Weekly Summary")
        print("=" * 50)
        run_weekly_report()
    else:
        print("=" * 50)
        print("📅 WEEKDAY MODE: Generating Daily Report")
        print("=" * 50)
        run_daily_report()


def run_daily_report():
    """Run the daily market movers report"""
    print("\nFetching S&P 500 daily market data...")
    stocks = fetch_sp500_data(weekly=False)
    
    if not stocks:
        raise ValueError("No stock data retrieved")
    
    print("\nCalculating top gainers and losers...")
    gainers, losers = get_top_movers(stocks, limit=20)
    
    print(f"Found {len(gainers)} gainers and {len(losers)} losers")
    
    if gainers:
        print("\nTop 5 Gainers:")
        for s in gainers[:5]:
            print(f"  {s['ticker']}: {s['change_percentage']}")
    
    if losers:
        print("\nTop 5 Losers:")
        for s in losers[:5]:
            print(f"  {s['ticker']}: {s['change_percentage']}")
    
    print("\nBuilding email...")
    html = build_email_html(gainers, losers)
    
    print("Sending email...")
    result = send_email(html, weekly=False)
    print(f"Email sent successfully! ID: {result.get('id')}")


def run_weekly_report():
    """Run the weekly summary report - top 20 gainers and losers for the week"""
    print("\nFetching S&P 500 weekly market data (5 trading days)...")
    stocks = fetch_sp500_data(weekly=True)
    
    if not stocks:
        raise ValueError("No stock data retrieved")
    
    print(f"\nFetched data for {len(stocks)} stocks")
    
    # Check how many trading days we captured
    if stocks:
        avg_days = sum(s.get('days_captured', 0) for s in stocks) / len(stocks)
        print(f"Average trading days captured: {avg_days:.1f}")
    
    print("\nCalculating top weekly gainers and losers...")
    gainers, losers = get_top_movers(stocks, limit=20)
    
    print(f"Found {len(gainers)} gainers and {len(losers)} losers")
    
    if gainers:
        print("\nTop 5 Weekly Gainers:")
        for s in gainers[:5]:
            print(f"  {s['ticker']}: {s['change_percentage']}")
    
    if losers:
        print("\nTop 5 Weekly Losers:")
        for s in losers[:5]:
            print(f"  {s['ticker']}: {s['change_percentage']}")
    
    print("\nBuilding weekly email...")
    html = build_weekly_email_html(gainers, losers)
    
    print("Sending email...")
    result = send_email(html, weekly=True)
    print(f"Email sent successfully! ID: {result.get('id')}")


if __name__ == "__main__":
    main()
