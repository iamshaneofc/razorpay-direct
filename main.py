from flask import Flask, request
import json
import os

app = Flask(__name__)

@app.route('/razorpay-webhook', methods=['POST'])
def webhook():
    raw_data = request.get_data(as_text=True)        # full raw JSON
    data = request.get_json(force=True) or {}

    if not data or data.get('event') != 'payment.captured':
        print("Ignored event:", data.get('event'))
        return "ok", 200

    p = data['payload']['payment']['entity']

    print("\n" + "═" * 80)
    print("NEW PAYMENT RECEIVED — FULL DETAILS")
    print("═" * 80)
    print(f"Time          : {__import__('datetime').datetime.now().strftime('%d-%b-%Y %I:%M %p')}")
    print(f"Amount        : ₹{p['amount']/100:,}")
    print(f"Payment ID    : {p['id']}")
    print(f"Status        : {p['status']}")
    print(f"Email         : {p.get('email') or '—'}")
    print(f"Contact       : {p.get('contact') or '—'}")
    print(f"Customer Name : {p.get('customer_name', '—')}")
    print(f"Method        : {p.get('method')}")
    print(f"Card/Network  : {p.get('card', {}).get('network', '—')}")
    print(f"Order ID      : {p.get('order_id') or '—'}")
    print(f"Description   : {p.get('description') or '—'}")
    
    # All notes (custom fields you pass from Odoo/website)
    notes = p.get('notes', {})
    if notes:
        print("Custom Notes:")
        for key, value in notes.items():
            print(f"   → {key} : {value}")

    print("Full Raw JSON (for debugging):")
    print(json.dumps(data, indent=2)[:1000])   # first 1000 chars
    print("═" * 80 + "\n")

    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))