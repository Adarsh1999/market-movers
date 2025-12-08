# S&P 500 Market Movers 📈

A beautiful, auto-updating website that displays daily S&P 500 top gainers and losers. Updated automatically every weekday after market close.

## ✨ Features

- 🟢 **Top 20 Gainers** - Stocks with highest daily gains
- 🔴 **Top 20 Losers** - Stocks with biggest daily losses
- 📊 **Market Summary** - Quick overview of market sentiment
- 📥 **CSV Downloads** - Export data for your own analysis
- 📋 **Copy to Clipboard** - Quick data sharing
- 🔍 **Search** - Find specific stocks instantly
- 📱 **Mobile Responsive** - Works on all devices
- 🌙 **Dark Theme** - Easy on the eyes
- ⏰ **Auto-Updates** - Refreshes daily via GitHub Actions

## 🚀 Live Demo

Visit: `https://YOUR-USERNAME.github.io/market-movers/`

## 🛠️ Setup

### 1. Fork or Clone This Repository

```bash
git clone https://github.com/YOUR-USERNAME/market-movers.git
cd market-movers
```

### 2. Enable GitHub Pages

1. Go to your repo → **Settings** → **Pages**
2. Under "Build and deployment", select **GitHub Actions**
3. Save changes

### 3. Run the Workflow

1. Go to your repo → **Actions** tab
2. Click **"Update Market Movers Website"**
3. Click **"Run workflow"** → **"Run workflow"**

The site will be live at `https://YOUR-USERNAME.github.io/market-movers/` within a few minutes!

## 📅 Schedule

The website automatically updates:
- **Time:** 4:30 PM ET (21:30 UTC)
- **Days:** Monday through Friday
- **Why:** Market closes at 4 PM ET, giving 30 minutes for data to settle

## 🏗️ How It Works

```
┌─────────────────────────────────────────────────────────────┐
│              GitHub Actions (4:30 PM ET, Mon-Fri)           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   1. Fetch S&P 500 data from Yahoo Finance (yfinance)       │
│   2. Calculate top 20 gainers and losers                    │
│   3. Generate static HTML with embedded data                │
│   4. Create downloadable CSV files                          │
│   5. Deploy to GitHub Pages                                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## 📁 Project Structure

```
market-movers/
├── generate_site.py          # Main site generator script
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── LICENSE                   # MIT License
└── .github/
    └── workflows/
        └── market-movers.yml # GitHub Actions workflow
```

## 🧪 Run Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Generate the site
python generate_site.py

# View the site
cd dist
python -m http.server 8000
# Open http://localhost:8000 in your browser
```

## 📊 Generated Files

After running, the `dist/` folder contains:

| File | Description |
|------|-------------|
| `index.html` | Main website |
| `data/gainers.csv` | Top 20 gainers in CSV format |
| `data/losers.csv` | Top 20 losers in CSV format |
| `data/all_stocks.csv` | All S&P 500 stocks sorted by performance |
| `data/data.json` | JSON data for programmatic access |

## 💰 Cost

| Service | Cost |
|---------|------|
| GitHub Pages Hosting | **FREE** |
| GitHub Actions | **FREE** (2,000 min/month) |
| Yahoo Finance Data | **FREE** |
| **Total** | **$0** |

## 🔄 Alternative: Email Reports

Want daily email reports instead? Check out the [`email-approach`](../../tree/email-approach) branch which sends beautiful HTML emails via Resend.

## 📈 Data Source

- **Provider:** Yahoo Finance via `yfinance` library
- **Coverage:** All S&P 500 stocks (~500 companies)
- **Update Frequency:** Daily (weekdays only)
- **No API key required!**

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## 📄 License

MIT License - feel free to use this for your own projects!

---

Made with ❤️ for stock market enthusiasts
