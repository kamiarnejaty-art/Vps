import requests
import sys

TOKEN = "BEHFJF0YAIALQLLOIEKEEMMOFWIJHEGGLPPEHZPXDPABVDUABKUXBJNAOOCFYHXL"

# آدرس عمومی سرورتو اینجا بذار (مثل https://rubika-bot.onrender.com)
WEBHOOK_URL = sys.argv[1] if len(sys.argv) > 1 else "https://your-app.onrender.com/webhook"

def set_webhook():
    url = f"https://botapi.rubika.ir/v3/{TOKEN}/updateBotEndpoint"
    data = {"endpoint": WEBHOOK_URL}
    
    try:
        r = requests.post(url, json=data, timeout=10)
        print(f"وضعیت: {r.status_code}")
        print(f"پاسخ: {r.json()}")
        
        if r.status_code == 200:
            print("✅ Webhook با موفقیت ثبت شد!")
        else:
            print("❌ خطا در ثبت Webhook")
    except Exception as e:
        print(f"❌ خطا: {e}")

if __name__ == "__main__":
    set_webhook()
