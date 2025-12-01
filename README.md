# Market Movers 📈

Automated daily email reports of top stock gainers and losers, delivered to your inbox every weekday at 4:30 PM ET.

## Features

- 🟢 Top 20 Stock Gainers
- 🔴 Top 20 Stock Losers  
- 📧 Beautiful HTML email format
- ⏰ Automatic delivery via GitHub Actions (Mon-Fri)
- 🔄 Manual trigger available for testing

## Setup

### 1. Get API Keys

| Service | URL | Free Tier |
|---------|-----|-----------|
| Alpha Vantage | [alphavantage.co/support/#api-key](https://www.alphavantage.co/support/#api-key) | 25 calls/day |
| Resend | [resend.com](https://resend.com) | 3,000 emails/month |

### 2. Configure GitHub Secrets

Go to your repo → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

Add these secrets:

- `ALPHA_VANTAGE_KEY` — Your Alpha Vantage API key
- `RESEND_API_KEY` — Your Resend API key  
- `EMAIL_TO` — Your email address (e.g., `your-email@example.com`)

### 3. Test Locally (Optional)

```bash
# Install dependencies
pip install -r requirements.txt

# Test API keys
python3 test_api_keys.py

# Test Resend email (requires EMAIL_TO)
python3 test_resend_email.py your-email@example.com

# Run the full script (requires all env vars)
export ALPHA_VANTAGE_KEY="your-key"
export RESEND_API_KEY="your-key"
export EMAIL_TO="your-email@example.com"
python3 market_movers.py
```

### 4. Push to GitHub

```bash
git add .
git commit -m "Add market movers automation"
git push origin main
```

### 5. Test the Workflow

1. Go to your repo → **Actions** tab
2. Click **"Daily Market Movers Email"**
3. Click **"Run workflow"** → **"Run workflow"** (to test manually)

## Schedule

The workflow runs automatically:
- **Time:** 4:30 PM ET (21:30 UTC)
- **Days:** Monday through Friday
- **Why:** Market closes at 4 PM ET, giving 30 minutes for data to update

## How It Works

```
┌─────────────────────────────────────────────────────────┐
│              GitHub Actions Cron Job                    │
│              (Runs 4:30 PM ET, Mon-Fri)                 │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   1. Fetch data from Alpha Vantage API                  │
│   2. Format as HTML table                               │
│   3. Send email via Resend                              │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Files

- `market_movers.py` - Main Python script
- `.github/workflows/market-movers.yml` - GitHub Actions workflow
- `test_api_keys.py` - Test script for API keys
- `test_resend_email.py` - Test script for Resend email

## Notes

- **Resend FROM address:** Uses `onboarding@resend.dev` on free tier. You can verify your own domain in Resend dashboard.
- **No runs on weekends/holidays:** Market's closed, so no emails sent.
- **Rate limits:** Alpha Vantage free tier allows 25 calls/day (we use 1 per day).

## License

MIT
