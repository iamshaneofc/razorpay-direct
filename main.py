from flask import Flask, request
import json
import logging
import sys
import os
from datetime import datetime

app = Flask(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

@app.route('/razorpay-webhook', methods=['POST'])
def webhook():
    data = request.get_json(force=True) or {}
    
    # Only process real successful payments
    if not data or data.get('event') != 'payment.captured':
        return "ok", 200

    p = data['payload']['payment']['entity']

    logging.info("\n" + "═" * 90)
    logging.info(" NEW PAYMENT FROM ODOO WEBSITE — BODHIH.COM")
    logging.info("═" * 90)
    logging.info(f"Time           : {datetime.now().strftime('%d %b %Y, %I:%M %p')}")
    logging.info(f"Amount         : ₹{p['amount']/100:,.2f}")
    logging.info(f"Payment ID     : {p['id']}")
    logging.info(f"Order ID       : {p.get('order_id', '—')}")
    logging.info(f"Customer Name  : {p.get('customer_name', '—')}")
    logging.info(f"Email          : {p.get('email') or p.get('notes', {}).get('user_email', '—')}")
    logging.info(f"Phone          : {p.get('contact', '—')}")
    logging.info(f"Payment Method : {p.get('method', '—').title()}")
    logging.info(f"Card/Network   : {p.get('card', {}).get('network', '—')} {p.get('card', {}).get('last4', '')}")
    logging.info(f"Description    : {p.get('description', '—')}")

    # All custom notes (this is where Odoo sends course name, batch, etc.)
    notes = p.get('notes', {})
    if notes:
        logging.info("Custom Fields from Odoo:")
        for key, value in notes.items():
            logging.info(f"   → {key:15} : {value}")

    # Full raw payload (for future debugging)
    logging.info("Full Raw Payload (first 800 chars):")
    logging.info(json.dumps(data, indent=2)[:800])
    logging.info("═" * 90 + "\n")

    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))