from rubka import Robot, Message
from rubka.button import ChatKeypadBuilder
from pyrubi import Client
from random import randint, choice
from collections import defaultdict
import asyncio
import sqlite3
import json
import time
from functools import lru_cache
from contextlib import contextmanager
# کامیت
# client = Client('own_session')
bot = Robot("BEHFJF0YAIALQLLOIEKEEMMOFWIJHEGGLPPEHZPXDPABVDUABKUXBJNAOOCFYHXL",web_hook='https://webhock-pmteam.runflare.run')

user_commands = defaultdict(lambda: {'count': 0, 'first_time': 0})
blocked_users = {}
blocked_notified = {}

def check_spam(user_id, command_name, max_count=3, time_window=4, block_duration=60):
    current_time = time.time()
    
    if user_id in blocked_users:
        if current_time < blocked_users[user_id]:
            return True, False
        else:
            del blocked_users[user_id]
            if user_id in blocked_notified:
                del blocked_notified[user_id]
    
    key = f"{user_id}_{command_name}"
    
    if key not in user_commands:
        user_commands[key] = {'count': 1, 'first_time': current_time}
        return False, False
    
    time_passed = current_time - user_commands[key]['first_time']
    
    if time_passed > time_window:
        user_commands[key] = {'count': 1, 'first_time': current_time}
        return False, False
    
    user_commands[key]['count'] += 1
    
    if user_commands[key]['count'] > max_count:
        blocked_users[user_id] = current_time + block_duration
        return True, True
    
    return False, False

PRODUCTION_RATE = {1: 10,2: 20,3: 35,4: 55,5: 80,6: 110,7: 150,8: 200,9: 260,10: 330}
def calculate_production(farm_lvl, last_time, current_time):
    minutes_passed = (current_time - last_time) // 60
    max_production = False
    if minutes_passed >= 60:
        minutes_passed = 60
        max_production = True
    rate = PRODUCTION_RATE.get(farm_lvl, 10)
    return minutes_passed * rate , max_production

@contextmanager
def get_db():
    conn = sqlite3.connect("/db/RubkaSaveMessage.db", timeout=10)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

user_cache = {}
cache_ttl = 300

def get_cached_user(user_id):
    if user_id in user_cache:
        data, timestamp = user_cache[user_id]
        if time.time() - timestamp < cache_ttl:
            return data
    return None

def set_cached_user(user_id, data):
    user_cache[user_id] = (data, time.time())

async def save_last_5_messages(user_id, chat_id, msg_id):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT messages_id_l FROM last_msg WHERE user_id_l = ? AND chat_id_l = ?",
            (user_id, chat_id)
        )
        result = cursor.fetchone()
        
        messages_list = json.loads(result[0]) if result else []
        messages_list.insert(0, msg_id)
        messages_list = messages_list[:5]
        
        cursor.execute("""
            INSERT INTO last_msg (user_id_l, chat_id_l, messages_id_l)
            VALUES (?, ?, ?)
            ON CONFLICT(user_id_l, chat_id_l)
            DO UPDATE SET messages_id_l = excluded.messages_id_l
        """, (user_id, chat_id, json.dumps(messages_list)))
        conn.commit()

async def find_user_by_msg_rep_id(user, msg_rep_id):
    for user_id, messages_json in user:
        if msg_rep_id in json.loads(messages_json):
            return user_id
    return None

@bot.on_message()
async def msg(_: Robot, message: Message):
    text = message.text
    user_id = message.sender_id
    chat_id = message.chat_id
    msg_id = message.message_id
    
    await save_last_5_messages(user_id, chat_id, msg_id)

    if user_id in blocked_users:
        current_time = time.time()
        if current_time < blocked_users[user_id]:
            return
        else:
            del blocked_users[user_id]
            if user_id in blocked_notified:
                del blocked_notified[user_id]
    
    commands_to_check = ['گردونه 🎲' ,'مزرعه 🌿' ,'مزرعه' , 'راهنمای مزرعه' , 'پول', 'گردونه', 'دستورات رول پلی 📘', 'دستورات', '/help', 'مزرعه', '/start', 'شروع', 'شروع رول پلی ✨','پینگ' , '/ping']
    
    if text in commands_to_check:
        is_blocked, should_notify = check_spam(user_id, text, max_count=3, time_window=5, block_duration=60)
        
        if is_blocked:
            if should_notify:
                await message.reply(
                    f'🚫 **شما تایم اوت شدید!** 🚫\n'
                    f'**⏱️ 60 ثانیه**'
                )
            return

    if text == '/start' and message.is_user:
        keypad = (ChatKeypadBuilder()
                  .row(ChatKeypadBuilder().button_simple(id='start_rp', text='شروع رول پلی ✨'))
                  .build())
        
        username = await bot.get_username(chat_id)
        return await bot.send_message(
            chat_id,
            text=(
                f'👋 **سلام داداش گُلم، {username}!** 👋\n\n'
                '🌟 **حمایت شما، دلگرمی ماست!** 🌟\n'
                'برای حمایت از ما، عضو کانال روبیکا شو:\n'
                '👇\n'
                '🔗 rubika.ir/PM_TEAM\n\n'
                '▶️ **اماده یکم خلاف کاری هستی؟** ▶️\n'
                'روی دکمه **"شروع"** کلیک کن!'
            ),
            chat_keypad=keypad
        )
    
    if text in ('شروع', 'شروع رول پلی ✨'):
        with get_db() as conn:
            cursor = conn.cursor()
            
            cursor.execute("SELECT user_id, user_name FROM rp_user WHERE user_id = ?", (user_id,))
            user = cursor.fetchone()
            
            if user:
                return await message.reply(
                    f'**💢 قبلا وارد رول پلی شدی 💢**\n'
                    f'**🔍 اسم شما -> {user[1]}**\n'
                    '🔹 دستور «`راهنما`» -> ارسال اطلاعات'
                )
            
            cursor.execute("SELECT sender_id_q FROM queue WHERE sender_id_q = ?", (user_id,))
            try:
                cursor.execute("INSERT INTO queue (sender_id_q, chat_id_q) VALUES (?, ?)", (user_id, chat_id))
                conn.commit()
                return await message.reply('**✏️ یک اسم دلخواه ارسال کنید ✏️**\n\nلغو -> 11')
            except:
                return await message.reply('**✏️ یک اسم دلخواه ارسال کنید ✏️**\n\nلغو -> 11')
    
    if text in ('دستورات رول پلی 📘', 'دستورات', '/help'):
        if message.is_user:
            keypad = (ChatKeypadBuilder()
                    .row(ChatKeypadBuilder().button_simple(id='gardone', text='گردونه 🎲') , ChatKeypadBuilder().button_simple(id='mazrae', text='مزرعه 🌿'))
                    .row(ChatKeypadBuilder().button_simple(id='inventory', text='موجودی 🧾'))
                    .build())
            
            return await bot.send_message(chat_id , '✨ دستورات ✨' , keypad)
    
    if text in ('پول' , '/pool'):
        with get_db() as conn:
            cursor = conn.cursor()
            
            if message.is_reply:
                msg_rep_id = message.reply_to_message_id
                cursor.execute(
                    "SELECT user_id_l, messages_id_l FROM last_msg WHERE chat_id_l = ?",
                    (chat_id,)
                )
                users = cursor.fetchall()
                user_rep_id = await find_user_by_msg_rep_id(users, msg_rep_id)
                
                if user_rep_id:
                    cursor.execute("SELECT user_money FROM rp_user WHERE user_id = ?", (user_rep_id,))
                    user = cursor.fetchone()
                    if user:
                        return await message.reply(f'**پول او : {user[0]}$ **')
            else:
                cursor.execute("SELECT user_money FROM rp_user WHERE user_id = ?", (user_id,))
                user = cursor.fetchone()
                if user:
                    return await message.reply(f'**پول شما : {user[0]}$ **')
        
        return await message.reply(
            '⭕ **داخل بازی نیستید** ⭕\n'
            'با ارسال دستور « `شروع` » وارد بازی شوید'
        )
    
    if text == '11':
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT sender_id_q FROM queue WHERE sender_id_q = ?", (user_id,))
            if cursor.fetchone():
                await message.reply('❕ **انتظار برای ارسال اسم لغو شد** ❕')
                cursor.execute("DELETE FROM queue WHERE sender_id_q = ?", (user_id,))
                conn.commit()
    
    if text in ('گردونه' , 'گردونه 🎲'):
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT cd_spin, user_money FROM rp_user WHERE user_id = ?", (user_id,))
            result = cursor.fetchone()
            
            if result:
                cd_time = int(result[0])
                current_time = int(message.time)
                
                if cd_time < current_time:
                    x = choice([True, False])
                    if x:
                        amount = randint(1, 1000)
                        new_money = result[1] + amount
                        
                        await message.reply(
                            '🟢 **گردونه موفقیت آمیز بود** 🟢\n'
                            f'**💸 دریافت : {amount}$ 🤑**'
                        )
                        
                        new_cd = str(current_time + 3600)
                        cursor.execute("UPDATE rp_user SET cd_spin = ?, user_money = ? WHERE user_id = ?",
                                    (new_cd, new_money, user_id))
                        conn.commit()
                        return
                    else:
                        return await message.reply(
                            '🔴 **گردونه موفقیت آمیز نبود** 🔴\n'
                            '**دوباره تلاش کن 😪**'
                        )
                else:
                    remaining_seconds = cd_time - current_time
                    remaining_minutes = remaining_seconds // 60
                    remaining_seconds = remaining_seconds % 60
                    
                    await message.reply(
                        f'⏳ **صبر کن رفیق!** ⏳\n'
                        f'➖➖➖➖➖➖➖\n'
                        f'🎡 **گردونه هنوز آماده نیست!**\n'
                        f'⏰ **زمان باقی‌مونده:** {remaining_minutes} دقیقه و {remaining_seconds} ثانیه\n'
                    )
            else:
                return await message.reply('⭕ **داخل بازی نیستید** ⭕')
            
    if text in ('پینگ' , '/ping'):
        start = time.time()
        msg = await message.reply('🏓 در حال محاسبه پینگ...')
        end = time.time()
        ping = int((end - start) * 1000)
        return await msg.edit(f'🏓 **پینگ شما:** {ping}ms')
    
    if text == 'راهنمای مزرعه':
        return await message.reply(
            f"🔹 `برداشت` -> برداشت محصول\n"
            f"🔹 `پک` -> بسته‌بندی محصول\n"
            f"🔹 `فروش` -> فروش محصولات\n"
            f"🔹 `ارتقا` -> سطح مزرعه\n"
            f"🔹 `اتوپک` -> خرید اتوپک"
        )

    if text in ('مزرعه' , 'مزرعه 🌿'):
        with get_db() as conn:
            cursor = conn.cursor()
            new_farm = ''

            user = cursor.execute("SELECT user_id FROM rp_user WHERE user_id = ?", (user_id,)).fetchone()
            if not(user):
                return await message.reply(
                    '⭕ **داخل بازی نیستید** ⭕\n'
                    'با ارسال دستور « `شروع` » وارد بازی شوید'
                )
            

            cursor.execute("SELECT * FROM user_farm_weed WHERE farm_id = ?", (user_id,))
            farm = cursor.fetchone()

            if not farm:
                new_farm = '**🌿مزرعه شما برپا شد🌿**'
                cursor.execute(
                    "INSERT INTO user_farm_weed (farm_id, last_harvest) VALUES (?, ?)",
                    (user_id, int(message.time))
                )
                conn.commit()
                farm = cursor.execute("SELECT * FROM user_farm_weed WHERE farm_id = ?", (user_id,)).fetchone()
            
            current_time = int(message.time)
            last_time = farm['last_harvest']
            pending = farm['pending_product']
            
            new_product, max_production = calculate_production(farm['farm_lvl'], last_time, current_time)
            total_pending = pending + new_product
            
            if new_product > 0:
                cursor.execute(
                    "UPDATE user_farm_weed SET pending_product = ?, last_harvest = ? WHERE farm_id = ?",
                    (total_pending, current_time, user_id)
                )
                conn.commit()
            
            harvested = farm['harvested_product'] if farm['harvested_product'] is not None else 0
            
            auto_pack = "فعال ✅" if farm['farm_auto_pack'] == 'yes' else "غیرفعال ❌"
            max_symbols = "ᴹᴬˣ" if max_production else " "

            return await message.reply(
                f'{new_farm}\n\n'
                f"🌾 **مزرعه وید** 🌾\n"
                f"ا➖➖➖➖➖➖➖ا\n"
                f"📊 **سطح:** {farm['farm_lvl']}\n"
                f"⚡ **نرخ تولید:** {PRODUCTION_RATE.get(farm['farm_lvl'])} گرم در دقیقه\n"
                f"📌 **محصول آماده برداشت:** {total_pending} گرم {max_symbols}\n"
                f"📦 **محصول برداشت شده:** {harvested} گرم\n"
                f"⚙️ **اتوپک:** {auto_pack}\n"
                f"ا➖➖➖➖➖➖➖ا\n"
                f"🔹 `راهنمای مزرعه` -> دستورات مربوط به مزرعه"
            )

    if text == 'برداشت':
        with get_db() as conn:
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM user_farm_weed WHERE farm_id = ?", (user_id,))
            farm = cursor.fetchone()
            
            if not farm:
                return await message.reply('❌ اول با دستور «مزرعه» یه مزرعه بساز!')
            
            current_time = int(message.time)
            last_time = farm['last_harvest']
            pending = farm['pending_product']
            
            new_product, max_production = calculate_production(farm['farm_lvl'], last_time, current_time)
            total_pending = pending + new_product
            
            if total_pending == 0:
                return await message.reply('**هیچ محصولی برای برداشت نیست! 🌾**\n صبر کن یه کم.')
            
            old_harvested = farm['harvested_product'] if farm['harvested_product'] is not None else 0
            
            new_harvested = old_harvested + total_pending
            
            cursor.execute(
                "UPDATE user_farm_weed SET pending_product = 0, harvested_product = ?, last_harvest = ? WHERE farm_id = ?",
                (new_harvested, current_time, user_id)
            )
            conn.commit()
            
            if farm['farm_auto_pack'] == 'yes':
                pass
            
            return await message.reply(
                f"✅ **{total_pending} گرم** محصول برداشت شد!\n"
                f"📦 ولی هنوز پک نشده!\n"
                f"🔹 با دستور «پک» محصولات رو بسته‌بندی کن تا بتونی بفروشیشون."
            )
    
    with get_db() as conn:
        cursor = conn.cursor()
        user_queue = cursor.execute("SELECT sender_id_q FROM queue WHERE sender_id_q = ?", (user_id,)).fetchone()
        if user_queue:
            if len(text) > 15:
                await message.reply('⭕ **اسم ارسالی شما طولانی است** ⭕\nلغو : 11')
            else:
                cursor.execute("SELECT user_name FROM rp_user")
                existing_names = {row[0] for row in cursor.fetchall()}
                
                if text not in existing_names:
                    reply_text = (
f'''
سلام {text} جان 😊
خوب گوش کن چی بهت میگم:👇

**🎲 با «گردونه» از شانست پول در بیار**
**🌿 یادت نره به «مزرعه» یه سر بزن**
**💰 اگه جنس پک شده داری، من خریدارم**

🔹 لیست دستورات رو ببین
🔹 تو گروه و خصوصی در دسترسـم

خوش بگذره 🤍
'''
                    )
                    
                    if message.is_user:
                        keypad = (ChatKeypadBuilder()
                                .row(ChatKeypadBuilder().button_simple(id='mine', text='دستورات رول پلی 📘') , ChatKeypadBuilder().button_simple(id = 'add' , text='افزوردن به گروه'))
                                .build())
                        await message.reply(text=reply_text, chat_keypad=keypad)
                    else:
                        await message.reply(reply_text)
                    
                    cursor.execute("DELETE FROM queue WHERE sender_id_q = ?", (user_id,))
                    cursor.execute(
                        "INSERT INTO rp_user (user_id, user_name, user_money, cd_spin) VALUES (?, ?, ?, ?)",
                        (user_id, text, 0, message.time)
                    )
                    conn.commit()
                else:
                    await message.reply('⭕ **اسم تکراری است** ⭕\nلغو : 11')

bot.run()
