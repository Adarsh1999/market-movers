# 🚀 Quick Start Guide

## Run Locally (3 Simple Steps)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Generate the Website
```bash
python generate_site.py
```

This will:
- Fetch S&P 500 data from Yahoo Finance
- Generate HTML, CSV files, and JSON
- Create everything in the `dist/` folder

### Step 3: View the Website
```bash
cd dist
python -m http.server 8000
```

Then open your browser and go to:
```
http://localhost:8000
```

---

## Alternative: Use Any Web Server

You can also use any of these:

```bash
# Python 3
cd dist && python -m http.server 8000

# Python 2
cd dist && python -m SimpleHTTPServer 8000

# Node.js (if you have it)
cd dist && npx http-server -p 8000

# PHP (if you have it)
cd dist && php -S localhost:8000
```

---

## What Gets Generated?

After running `python generate_site.py`, you'll see:

```
dist/
├── index.html          ← Main website (open this!)
├── data/
    ├── data.json       ← JSON API (daily + weekly)
    ├── daily/
    │   ├── gainers.csv     ← Top 20 daily gainers
    │   ├── losers.csv      ← Top 20 daily losers
    │   └── all_stocks.csv  ← All S&P 500 stocks (daily)
    ├── charts/
    │   └── AAPL.json       ← Candlestick chart data (top movers only)
    └── weekly/
        ├── gainers.csv     ← Top 20 weekly gainers (completed Mon-Fri week)
        ├── losers.csv      ← Top 20 weekly losers (completed Mon-Fri week)
        └── all_stocks.csv  ← All S&P 500 stocks (weekly)
```

---

## Troubleshooting

**Problem:** `pip: command not found`
**Solution:** Use `pip3` instead:
```bash
pip3 install -r requirements.txt
python3 generate_site.py
```

**Problem:** `yfinance` installation fails
**Solution:** Try upgrading pip first:
```bash
pip install --upgrade pip
pip install yfinance
```

**Problem:** Port 8000 already in use
**Solution:** Use a different port:
```bash
python -m http.server 9000
# Then visit http://localhost:9000
```
