#!/usr/bin/env python3
"""Test Resend API by sending a test email"""

import os
import requests
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

RESEND_API_KEY = os.environ.get("RESEND_API_KEY")
RESEND_URL = "https://api.resend.com/emails"

# Get email from command line or environment
EMAIL_TO = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("EMAIL_TO")

if not EMAIL_TO:
    print("❌ Please provide an email address in .env or as argument:")
    print("   python3 test_resend_email.py your-email@example.com")
    sys.exit(1)

def test_resend_email():
    """Test Resend API by sending a test email"""
    print("=" * 60)
    print("Testing Resend API with test email...")
    print("=" * 60)
    print(f"Sending test email to: {EMAIL_TO}")
    
    if not RESEND_API_KEY:
        print("❌ RESEND_API_KEY not found in .env")
        return False

    payload = {
        "from": "Market Movers <onboarding@resend.dev>",
        "to": [EMAIL_TO],
        "subject": "🧪 Test Email - Market Movers Setup",
        "html": """
        <html>
        <body style="font-family: Arial, sans-serif; padding: 20px;">
            <h2>✅ Resend API Test Successful!</h2>
            <p>If you're reading this, your Resend API key is working correctly.</p>
            <p>Your Market Movers daily emails will be sent to this address.</p>
        </body>
        </html>
        """
    }
    
    headers = {
        "Authorization": f"Bearer {RESEND_API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(RESEND_URL, json=payload, headers=headers, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Resend API Key: WORKING")
            print(f"   Email ID: {result.get('id')}")
            print(f"   Check your inbox at: {EMAIL_TO}")
            return True
        else:
            print(f"❌ Resend API Error:")
            print(f"   Status Code: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Resend API Request Failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Resend API Error: {e}")
        return False

if __name__ == "__main__":
    test_resend_email()
