# S&P 500 Market Movers 📈

Automated daily email reports of top S&P 500 stock gainers and losers, delivered to your inbox every weekday at 4:30 PM ET.

## Features

- 🟢 Top 20 S&P 500 Gainers
- 🔴 Top 20 S&P 500 Losers
- 📧 Beautiful HTML email format
- ⏰ Automatic delivery via GitHub Actions (Mon-Fri)
- 👥 Support for multiple email recipients
- 🔄 Manual trigger available for testing

## Setup

### 1. Get Resend API Key

| Service | URL | Free Tier |
|---------|-----|-----------|
| Resend | [resend.com](https://resend.com) | 3,000 emails/month |

### 2. Configure GitHub Secrets

Go to your repo → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

Add these **2 secrets**:

| Secret Name | Value | Example |
|-------------|-------|---------|
| `RESEND_API_KEY` | Your Resend API key | `re_xxxx...` |
| `EMAIL_TO` | Email recipient(s), comma-separated for multiple | `user1@gmail.com,user2@gmail.com` |

**⚠️ Important for Resend Free Tier:**
- On the free tier, you can only send to your own email (the one you signed up with)
- To send to other recipients, verify a domain at [resend.com/domains](https://resend.com/domains)

### 3. Test Locally (Optional)

```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << EOF
RESEND_API_KEY=your-resend-key
EMAIL_TO=your-email@example.com
EMAIL_FROM=Market Movers <onboarding@resend.dev>
EOF

# Run the script
python3 market_movers.py
```

**For multiple recipients locally:**
```bash
EMAIL_TO=user1@gmail.com,user2@gmail.com,user3@gmail.com
```

### 4. Push to GitHub

```bash
git add .
git commit -m "Add S&P 500 market movers automation"
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
- **Why:** Market closes at 4 PM ET, giving 30 minutes for data to settle

## How It Works

```
┌─────────────────────────────────────────────────────────┐
│              GitHub Actions Cron Job                    │
│              (Runs 4:30 PM ET, Mon-Fri)                 │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   1. Fetch S&P 500 data from Yahoo Finance (yfinance)   │
│   2. Calculate top gainers and losers                   │
│   3. Format as HTML table                               │
│   4. Send email via Resend to all recipients            │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Files

```
market-movers/
├── market_movers.py              # Main Python script
├── requirements.txt              # Python dependencies
├── .env                          # Local environment variables (not committed)
├── .env.example                  # Example environment file
├── .gitignore                    # Git ignore rules
└── .github/
    └── workflows/
        └── market-movers.yml     # GitHub Actions workflow
```

## GitHub Secrets Summary

| Secret | Required | Description |
|--------|----------|-------------|
| `RESEND_API_KEY` | ✅ Yes | Your Resend API key for sending emails |
| `EMAIL_TO` | ✅ Yes | Recipient email(s), comma-separated for multiple |

## Notes

- **Data Source:** Yahoo Finance via `yfinance` library (no API key needed)
- **Email Service:** Resend (3,000 free emails/month - you need ~22/month max)
- **No API rate limits:** Unlike Alpha Vantage, yfinance has no daily limits
- **Resend FROM address:** Uses `onboarding@resend.dev` on free tier

## Example Email

The email includes:
- 📈 S&P 500 Market Movers header with date
- 🟢 Top 20 Gainers table (Symbol, Price, Change %, Volume)
- 🔴 Top 20 Losers table (Symbol, Price, Change %, Volume)
- Data source footer

## License

MIT
