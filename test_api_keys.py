#!/usr/bin/env python3
"""Test script to verify Alpha Vantage and Resend API keys work"""

import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
ALPHA_VANTAGE_KEY = os.environ.get("ALPHA_VANTAGE_KEY")
RESEND_API_KEY = os.environ.get("RESEND_API_KEY")

if not ALPHA_VANTAGE_KEY or not RESEND_API_KEY:
    print("❌ Missing API keys in .env file")
    print("   Please ensure ALPHA_VANTAGE_KEY and RESEND_API_KEY are set in .env")
    exit(1)

ALPHA_VANTAGE_URL = "https://www.alphavantage.co/query"
RESEND_URL = "https://api.resend.com/emails"


def test_alpha_vantage():
    """Test Alpha Vantage API"""
    print("=" * 60)
    print("Testing Alpha Vantage API...")
    print("=" * 60)
    
    params = {
        "function": "TOP_GAINERS_LOSERS",
        "apikey": ALPHA_VANTAGE_KEY
    }
    
    try:
        response = requests.get(ALPHA_VANTAGE_URL, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        # Check for API errors
        if "Error Message" in data:
            print(f"❌ Alpha Vantage Error: {data['Error Message']}")
            return False
        
        if "Note" in data:
            print(f"⚠️  Alpha Vantage Note: {data['Note']}")
            return False
        
        if "top_gainers" in data and "top_losers" in data:
            gainers_count = len(data.get("top_gainers", []))
            losers_count = len(data.get("top_losers", []))
            print(f"✅ Alpha Vantage API Key: WORKING")
            print(f"   - Top Gainers: {gainers_count} stocks")
            print(f"   - Top Losers: {losers_count} stocks")
            print(f"   - Last Updated: {data.get('last_updated', 'N/A')}")
            return True
        else:
            print(f"❌ Unexpected response structure: {json.dumps(data, indent=2)}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Alpha Vantage API Request Failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Alpha Vantage API Error: {e}")
        return False


def test_resend():
    """Test Resend API"""
    print("\n" + "=" * 60)
    print("Testing Resend API...")
    print("=" * 60)
    
    # We'll just verify the API key is valid by checking API status
    # or attempting a minimal request
    headers = {
        "Authorization": f"Bearer {RESEND_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Try to get API key info or send a test email
    # Resend doesn't have a simple "verify key" endpoint, so we'll try
    # to send a minimal test email (but we need an email address)
    print("⚠️  Resend API key verification requires an email address.")
    print("   The key format looks correct, but full verification")
    print("   requires sending a test email.")
    print(f"   API Key: {RESEND_API_KEY[:20]}...")
    
    # Check if we can at least validate the format
    if RESEND_API_KEY.startswith("re_") and len(RESEND_API_KEY) > 20:
        print("✅ Resend API Key: Format looks valid")
        print("   (Full verification requires EMAIL_TO to be set)")
        return True
    else:
        print("❌ Resend API Key: Invalid format")
        return False


if __name__ == "__main__":
    print("\n🔑 API Key Testing Script\n")
    
    alpha_ok = test_alpha_vantage()
    resend_ok = test_resend()
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Alpha Vantage: {'✅ WORKING' if alpha_ok else '❌ FAILED'}")
    print(f"Resend:        {'✅ VALID FORMAT' if resend_ok else '❌ INVALID'}")
    print("\n")
