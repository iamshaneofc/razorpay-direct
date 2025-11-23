from flask import Flask, request
import json
import logging
import sys

app = Flask(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

@app.route('/razorpay-webhook', methods=['POST'])
def webhook():
    data = request.get_json(force=True) or {}
    
    if data.get('event') != 'payment.captured':
        return "ok", 200

    p = data['payload']['payment']['entity']
    
    logging.info("\n" + "═" * 80)
    logging.info("NEW PAYMENT — BODHIH.COM")
    logging.info(f"₹{p['amount']/100:,} | {p.get('email') or p.get('notes',{}).get('user_email','—')} | {p['id']}")
    logging.info("═" * 80)

    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))