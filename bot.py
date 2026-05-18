from rubka import Robot
from rubka.context import Message

# توکن ربات روبیکا
TOKEN = "BEHFJF0YAIALQLLOIEKEEMMOFWIJHEGGLPPEHZPXDPABVDUABKUXBJNAOOCFYHXL"

# راه‌اندازی ربات
bot = Robot(token=TOKEN)

# ========== هندلر استارت ==========
@bot.on_message(commands=["start"])
def start_handler(bot: Robot, message: Message):
    message.reply("سلام! 🌟\nربات من با Rubka روشن شد!")

# ========== هندلر راهنما ==========
@bot.on_message(commands=["help"])
def help_handler(bot: Robot, message: Message):
    help_text = """
❓ **راهنما:**

/start - شروع مجدد
/help - این راهنما
/about - درباره ربات

🎵 میتونی کلمه مورد نظرت رو بفرسی تا ویدیوهاش رو از تیک‌تاک بگیرم!
"""
    message.reply(help_text)

# ========== هندلر درباره ==========
@bot.on_message(commands=["about"])
def about_handler(bot: Robot, message: Message):
    message.reply("🤖 ربات جستجوگر تیک‌تاک\nنسخه 1.0\nساخته شده با Rubka")

# ========== پاسخ به پیام‌های معمولی ==========
@bot.on_message()
def echo_handler(bot: Robot, message: Message):
    text = message.text
    if text:
        message.reply(f"شما گفتید: {text}\n\nبرای دیدن راهنما /help رو بفرست.")
    else:
        message.reply("فقط متن رو میتونم جواب بدم!")

# ========== اجرا ==========
print("=" * 40)
print("🤖 ربات روبیکا روشن شد!")
print(f"🔑 توکن: {TOKEN[:20]}...")
print("=" * 40)

bot.run()
