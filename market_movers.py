import os
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- CONFIG (from GitHub Secrets) ---
ALPHA_VANTAGE_KEY = os.environ.get("ALPHA_VANTAGE_KEY")
RESEND_API_KEY = os.environ.get("RESEND_API_KEY")
EMAIL_TO = os.environ.get("EMAIL_TO")  # Your email address
EMAIL_FROM = os.environ.get("EMAIL_FROM", "Market Movers <onboarding@resend.dev>")

ALPHA_VANTAGE_URL = "https://www.alphavantage.co/query"
RESEND_URL = "https://api.resend.com/emails"


def fetch_market_movers():
    """Fetch top gainers and losers from Alpha Vantage"""
    params = {
        "function": "TOP_GAINERS_LOSERS",
        "apikey": ALPHA_VANTAGE_KEY
    }
    response = requests.get(ALPHA_VANTAGE_URL, params=params, timeout=30)
    response.raise_for_status()
    return response.json()


def build_html_table(stocks, is_gainers=True):
    """Build an HTML table for the stock data"""
    color = "#22c55e" if is_gainers else "#ef4444"
    title = "🟢 Top 20 Gainers" if is_gainers else "🔴 Top 20 Losers"
    
    rows = ""
    for i, stock in enumerate(stocks[:20], 1):
        change_pct = stock["change_percentage"]
        rows += f"""
        <tr style="border-bottom: 1px solid #e5e7eb;">
            <td style="padding: 8px; text-align: center;">{i}</td>
            <td style="padding: 8px; font-weight: bold;">{stock["ticker"]}</td>
            <td style="padding: 8px; text-align: right;">${float(stock["price"]):.2f}</td>
            <td style="padding: 8px; text-align: right; color: {color};">{change_pct}</td>
            <td style="padding: 8px; text-align: right;">{int(stock["volume"]):,}</td>
        </tr>
        """
    
    return f"""
    <div style="margin-bottom: 30px;">
        <h2 style="color: #1f2937; margin-bottom: 10px;">{title}</h2>
        <table style="width: 100%; border-collapse: collapse; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 14px;">
            <thead>
                <tr style="background-color: #f3f4f6;">
                    <th style="padding: 10px; text-align: center; width: 50px;">#</th>
                    <th style="padding: 10px; text-align: left;">Symbol</th>
                    <th style="padding: 10px; text-align: right;">Price</th>
                    <th style="padding: 10px; text-align: right;">Change %</th>
                    <th style="padding: 10px; text-align: right;">Volume</th>
                </tr>
            </thead>
            <tbody>
                {rows}
            </tbody>
        </table>
    </div>
    """


def build_email_html(data):
    """Build the complete email HTML"""
    last_updated = data.get("last_updated", "N/A")
    today = datetime.now().strftime("%A, %B %d, %Y")
    
    gainers_table = build_html_table(data["top_gainers"], is_gainers=True)
    losers_table = build_html_table(data["top_losers"], is_gainers=False)
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; background-color: #ffffff;">
        <div style="text-align: center; margin-bottom: 30px;">
            <h1 style="color: #1f2937; margin-bottom: 5px;">📈 US Market Movers</h1>
            <p style="color: #6b7280; margin: 0;">{today}</p>
            <p style="color: #9ca3af; font-size: 12px; margin-top: 5px;">Last updated: {last_updated}</p>
        </div>
        
        {gainers_table}
        {losers_table}
        
        <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #e5e7eb; text-align: center; color: #9ca3af; font-size: 12px;">
            <p>Data source: Alpha Vantage | US Stock Market</p>
        </div>
    </body>
    </html>
    """


def send_email(html_content):
    """Send email via Resend API"""
    today = datetime.now().strftime("%b %d, %Y")
    
    payload = {
        "from": EMAIL_FROM,
        "to": [EMAIL_TO],
        "subject": f"📈 Market Movers - {today}",
        "html": html_content
    }
    
    headers = {
        "Authorization": f"Bearer {RESEND_API_KEY}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(RESEND_URL, json=payload, headers=headers, timeout=30)
    response.raise_for_status()
    return response.json()


def main():
    print("Fetching market data...")
    data = fetch_market_movers()
    
    if "top_gainers" not in data:
        raise ValueError(f"Invalid API response: {data}")
    
    print("Building email...")
    html = build_email_html(data)
    
    print("Sending email...")
    result = send_email(html)
    print(f"Email sent successfully! ID: {result.get('id')}")


if __name__ == "__main__":
    main()

