from rubpy import Bot

TOKEN = "BEHFJF0YAIALQLLOIEKEEMMOFWIJHEGGLPPEHZPXDPABVDUABKUXBJNAOOCFYHXL"

# حالت Polling رو با use_webhook=False فعال کن
bot = Bot(token=TOKEN, use_webhook=False)

@bot.on_message(commands="start")
async def start_handler(update):
    await update.reply("سلام! ربات با حالت پولینگ (فقط برای تست) کار می‌کنه.")

if __name__ == "__main__":
    print("ربات با روش Polling روشن شد...")
    # متد run خودش حلقه Polling رو شروع می‌کنه
    bot.run()
