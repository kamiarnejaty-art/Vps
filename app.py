from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

TOKEN = "BEHFJF0YAIALQLLOIEKEEMMOFWIJHEGGLPPEHZPXDPABVDUABKUXBJNAOOCFYHXL"

# ========== هندلر Webhook ==========
@app.route('/webhook', methods=['POST'])
def webhook():
    # دریافت داده از روبیکا
    data = request.get_json()
    print(f"📨 داده دریافت شد: {data}")
    
    # پردازش پیام
    if 'new_message' in data:
        msg = data['new_message']
        chat_id = msg.get('chat_id')
        text = msg.get('text', '')
        
        print(f"📨 پیام از {chat_id}: {text}")
        
        # پاسخ به دستور /start
        if text == '/start':
            send_message(chat_id, "سلام! 🌟\nربات با Webhook روشن شد!")
        elif text:
            send_message(chat_id, f"شما گفتید: {text}")
    
    return jsonify({"status": "ok"}), 200

# ========== تابع ارسال پیام ==========
def send_message(chat_id, text):
    url = f"https://botapi.rubika.ir/v3/{TOKEN}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": text
    }
    try:
        r = requests.post(url, json=data, timeout=10)
        print(f"✅ پیام ارسال شد: {r.status_code}")
    except Exception as e:
        print(f"❌ خطا در ارسال: {e}")

# ========== ثبت Webhook در روبیکا ==========
def set_webhook(webhook_url):
    url = f"https://botapi.rubika.ir/v3/{TOKEN}/updateBotEndpoint"
    data = {"endpoint": webhook_url}
    try:
        r = requests.post(url, json=data, timeout=10)
        print(f"🔗 Webhook ثبت شد: {r.status_code} - {r.json()}")
        return True
    except Exception as e:
        print(f"❌ خطا در ثبت Webhook: {e}")
        return False

# ========== اجرا ==========
if __name__ == "__main__":
    import sys
    
    # آدرس Webhook رو از ورودی می‌گیریم یا از环境变量
    webhook_url = sys.argv[1] if len(sys.argv) > 1 else None
    
    if webhook_url:
        set_webhook(webhook_url)
    
    print("🤖 ربات Webhook در حال اجراست...")
    print("📍 آدرس Webhook رو توی روبیکا ثبت کن")
    app.run(host="0.0.0.0", port=8000)
