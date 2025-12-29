import time
import os
import threading

# Modules စစ်ဆေးခြင်း
try:
    from telebot import TeleBot, types
    from gatet import Tele
    from hit_sender import send
    print("✅ Libraries Loaded Successfully")
except ImportError as e:
    print(f"❌ Error: {e}")
    print("👉 Please run: pip3 install pyTelegramBotAPI requests func_timeout")
    exit()

# ==========================================
# 👇 TOKEN ထည့်ရန်
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
    except:
        return False

@bot.message_handler(commands=["start"])
def start(message):
    if not is_allowed(message): return
    bot.reply_to(message, "✅ <b>Bot is Online!</b>\n\nUsage:\n<code>/mt cc|mm|yy|cvc</code>\n<code>/mass</code> (Bulk 10)", parse_mode="HTML")

@bot.message_handler(commands=['gfemin'])
def send_hits_file(message):
    if not is_allowed(message): return
    if os.path.exists("gfemin.txt"):
        with open("gfemin.txt", "rb") as f:
            bot.send_document(message.chat.id, f, caption="✅ <b>Hits File</b>", parse_mode="HTML")
    else:
        bot.reply_to(message, "No hits saved yet! ❌")

@bot.message_handler(commands=['cleargfemin'])
def clear_hits(message):
    if not is_allowed(message): return
    if os.path.exists("gfemin.txt"):
        os.remove("gfemin.txt")
        bot.reply_to(message, "🗑️ File cleared!")
    else:
        bot.reply_to(message, "File already empty.")

# ===========================
# 🔥 1. MASS CHECK STATUS (EMOJI ONLY) 🔥
# ===========================
def get_mass_status(raw_response):
    if "Payment Successful" in raw_response:
        return '✅'
    elif "funds" in raw_response:
        return '♻️'
    elif "security code" in raw_response:
        return '✅' # CCN is technically Live
    elif "action" in raw_response or "3D" in raw_response:
        return '⚠️' # 3DS
    else:
        return '⛔' # Declined

# ===========================
# 🔥 2. SINGLE CHECK STATUS (FULL TEXT) 🔥
# ===========================
def get_single_status(raw_response):
    if "Payment Successful" in raw_response:
        return 'Transactions Successful 🥵'
    elif "funds" in raw_response:
        return 'Insufficient Funds 🍃'
    elif "security code" in raw_response:
        return 'CCN Live ✅'
    elif "action" in raw_response or "3D" in raw_response:
        return '3DS Required ⚠️'
    else:
        return 'Declined ❌' 

# ===========================
# MASS CHECKER (/mass)
# ===========================
@bot.message_handler(commands=['mass'])
def mass_check(message):
    if not is_allowed(message): return
    t = threading.Thread(target=process_mass, args=(message,))
    t.start()

def process_mass(message):
    try:
        input_text = message.text.replace('/mass', '').strip()
        if not input_text:
            bot.reply_to(message, "⚠️ <b>Error:</b> Please paste cards!\nExample:\n/mass\ncc|mm|yy|cvc\ncc|mm|yy|cvc", parse_mode="HTML")
            return

        cards = [line.strip() for line in input_text.split('\n') if line.strip()]
        if len(cards) > 10: cards = cards[:10]

        status_list = []
        for cc in cards:
            status_list.append(f"<code>{cc}</code>  ⏳") 

        status_message = "\n".join(status_list)
        msg = bot.reply_to(message, f"🔄 <b>Mass Check Started...</b>\n\n{status_message}", parse_mode="HTML")
        
        hits = 0
        username = message.from_user.username or "NoUsername"

        for index, cc in enumerate(cards):
            try:
                status_list[index] = f"<code>{cc}</code>  🔄"
                current_text = "\n".join(status_list)
                try:
                    bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id, text=f"🔄 <b>Processing...</b>\n\n{current_text}", parse_mode="HTML")
                except: pass

                # ကဒ်စစ်မယ်
                raw_response = str(Tele(cc))
                
                # 🔥 MASS အတွက် EMOJI Status ကိုခေါ်သုံးမယ်
                clean_status = get_mass_status(raw_response)

                status_list[index] = f"<code>{cc}</code>  {clean_status}"
                
                # Save Logic (✅, ♻️, ⚠️ ပါရင် Save မယ်)
                if "✅" in clean_status or "♻️" in clean_status or "⚠️" in clean_status:
                    hits += 1
                    with open("gfemin.txt", "a") as f:
                        f.write(f"{cc} | {clean_status}\n")
                    try:
                        # Mass Hit မိရင်လည်း Send Sender နဲ့ ပို့ချင်ရင် ဒီမှာဖွင့်ပါ
                        # send_response = send(cc, "Hit Found in Mass", username, 0)
                        # bot.reply_to(message, send_response, parse_mode="HTML")
                        pass
                    except: pass
                
                try:
                    current_text = "\n".join(status_list)
                    bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id, text=f"🔄 <b>Processing...</b>\n\n{current_text}", parse_mode="HTML")
                except: pass

            except Exception as e:
                print(f"Check Error: {e}")

        final_text = "\n".join(status_list)
        bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id, text=f"✅ <b>Mass Check Completed!</b>\n\nHits: {hits}\n\n{final_text}", parse_mode="HTML")

    except Exception as e:
        print(f"Mass Error: {e}")

# ===========================
# SINGLE CHECKER (/mt)
# ===========================
@bot.message_handler(commands=['mt'])
def check_card(message):
    if not is_allowed(message): return
    try:
        if len(message.text.split('/mt', 1)) < 2 or not message.text.split('/mt', 1)[1].strip():
            bot.reply_to(message, "⚠️ <b>Format Error!</b>\nUsage: <code>/mt cc|mm|yy|cvc</code>", parse_mode="HTML")
            return
            
        cc = message.text.split('/mt', 1)[1].strip()
        msg = bot.reply_to(message, "Checking...")
        
        start_time = time.time()
        raw_response = str(Tele(cc))
        time_taken = round(time.time() - start_time, 2)
        
        print(f"Checked: {cc} -> {raw_response}")

        # 🔥 SINGLE အတွက် Full Text Status ကိုခေါ်သုံးမယ်
        clean_status = get_single_status(raw_response)

        # Save Logic
        if "Successful" in clean_status:
            with open("gfemin.txt", "a") as f:
                f.write(f"{cc} | Transactions Successful 🥵\n")
        elif "Funds" in clean_status:
            with open("gfemin.txt", "a") as f:
                f.write(f"{cc} | Insufficient Funds 🍃\n")
        elif "3DS" in clean_status:
            with open("gfemin.txt", "a") as f:
                f.write(f"{cc} | 3DS Required ⚠️\n")

        username = message.from_user.username or "NoUsername"
        try:
            send_response = send(cc, clean_status, username, time_taken)
            bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id, text=send_response, parse_mode="HTML")
        except Exception as e:
            bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id, text=f"<b>Card:</b> <code>{cc}</code>\n<b>Status:</b> {clean_status}\n<b>Time:</b> {time_taken}s")

    except Exception as e:
        print(f"Single Check Error: {e}")

print("✅ Bot Started & Polling...")
bot.infinity_polling(timeout=25, long_polling_timeout=5)
