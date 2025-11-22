from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/razorpay-webhook', methods=['POST'])
def webhook():
    data = request.get_json(force=True)
    if not data or data.get('event') != 'payment.captured':
        return "ok", 200
        
    p = data['payload']['payment']['entity']
    
    # This will show in Render logs forever
    print("\n" + "═"*60)
    print("NEW PAYMENT RECEIVED!")
    print(f"₹{p['amount']/100} | {p.get('email') or p.get('notes',{}).get('user_email','—')} | {p.get('contact','—')} | {p['id']}")
    print("═"*60 + "\n")
    
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))