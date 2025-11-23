from flask import Flask, request
import json
import logging
import sys
import os                      # ← this was missing

app = Flask(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

@app.route('/razorpay-webhook', methods=['POST'])
def webhook():
    data = request.get_json(force=True) or {}
    
    if not data or data.get('event') != 'payment.captured':
        return "ok", 200

    p = data['payload']['payment']['entity']
    
    logging.info("\n" + "═" * 80)
    logging.info("NEW PAYMENT RECEIVED — BODHIH.COM")
    logging.info(f"Amount     : ₹{p['amount']/100:,}")
    logging.info(f"Email      : {p.get('email') or p.get('notes',{}).get('user_email','—')}")
    logging.info(f"Contact    : {p.get('contact','—')}")
    logging.info(f"Payment ID : {p['id']}")
    if p.get('notes'):
        logging.info("Notes:")
        for k, v in p['notes'].items():
            logging.info(f"   → {k}: {v}")
    logging.info("═" * 80)

    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))