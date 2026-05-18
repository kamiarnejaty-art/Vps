from rubka import Robot
from rubka.context import Message
from rubka.button import InlineBuilder
from rubka.keypad import ChatKeypadBuilder
import asyncio

TOKEN = "BEHFJF0YAIALQLLOIEKEEMMOFWIJHEGGLPPEHZPXDPABVDUABKUXBJNAOOCFYHXL"

bot = Robot(token=TOKEN)

# ========== هندلر استارت ==========
@bot.on_message(commands=["start"])
async def start_handler(bot: Robot, message: Message):
    # کیبورد چت (دکمه‌های پایین صفحه)
    keypad = ChatKeypadBuilder().row(
        ChatKeypadBuilder().button(id="info", text="📊 اطلاعات"),
        ChatKeypadBuilder().button(id="help", text="❓ راهنما")
    ).row(
        ChatKeypadBuilder().button(id="search", text="🔍 جستجو")
    ).build()
    
    await message.reply_keypad(
        "سلام! به ربات من خوش آمدی! 🎉\n\nاز دکمه‌ها استفاده کن:",
        keypad
    )

# ========== هندلر دکمه‌های چت ==========
@bot.on_message(commands=["info"])
async def info_handler(bot: Robot, message: Message):
    await message.reply("📊 **اطلاعات ربات**\nنسخه: 1.0\nساخته شده با Rubka")

@bot.on_message(commands=["help"])
async def help_handler(bot: Robot, message: Message):
    await message.reply("❓ **راهنما**\n/start - شروع مجدد\n/menu - منوی دکمه‌ای")

# ========== منوی اینلاین (دکمه شیشه‌ای) ==========
@bot.on_message(commands=["menu"])
async def menu_handler(bot: Robot, message: Message):
    builder = InlineBuilder()
    keyboard = builder.row(
        builder.button_simple(id="btn1", text="🎵 تیک‌تاک"),
        builder.button_simple(id="btn2", text="📌 پینترست")
    ).row(
        builder.button_simple(id="exit", text="❌ خروج")
    ).build()
    
    await message.reply_inline("منوی اصلی رو انتخاب کن:", keyboard)

# ========== هندلر کال‌بک دکمه‌های اینلاین ==========
@bot.on_callback("btn1")
async def btn1_callback(bot: Robot, message: Message):
    await message.reply("شما گزینه تیک‌تاک رو انتخاب کردید!")

@bot.on_callback("btn2")
async def btn2_callback(bot: Robot, message: Message):
    await message.reply("شما گزینه پینترست رو انتخاب کردید!")

@bot.on_callback("exit")
async def exit_callback(bot: Robot, message: Message):
    await message.delete()

# ========== ارسال عکس ==========
@bot.on_message(commands=["photo"])
async def photo_handler(bot: Robot, message: Message):
    await bot.send_image(message.chat_id, "path/to/image.jpg", caption="این یک عکس است")

# ========== ارسال ویدیو ==========
@bot.on_message(commands=["video"])
async def video_handler(bot: Robot, message: Message):
    await bot.send_video(message.chat_id, "path/to/video.mp4", caption="این یک ویدیو است")

# ========== اجرا ==========
print("🤖 ربات روشن شد!")
asyncio.run(bot.run())
