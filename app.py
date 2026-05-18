from flask import Flask, request, jsonify
import requests
import json
import os

app = Flask(__name__)

TOKEN = "BEHFJF0YAIALQLLOIEKEEMMOFWIJHEGGLPPEHZPXDPABVDUABKUXBJNAOOCFYHXL"

# ========== هندلر Webhook ==========
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print(f"📨 دریافت: {data}")
    
    if 'new_message' in data:
        msg = data['new_message']
        chat_id = msg.get('chat_id')
        text = msg.get('text', '')
        
        if text == '/start':
            send_message(chat_id, "سلام! ربات Webhook روشن شد! 🎉")
        elif text:
            send_message(chat_id, f"شما گفتید: {text}")
    
    return jsonify({"status": "ok"}), 200

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "alive"}), 200

def send_message(chat_id, text):
    url = f"https://botapi.rubika.ir/v3/{TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": text}
    try:
        r = requests.post(url, json=data, timeout=10)
        print(f"✅ ارسال شد: {r.status_code}")
    except Exception as e:
        print(f"❌ خطا: {e}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
