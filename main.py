import time
import os
import threading # Mass Check အတွက် Threading လိုအပ်ပါတယ်
from telebot import TeleBot, types
from gatet import Tele
from hit_sender import send  

admin_name = "@Rusisvirus"

# ==========================================
# 👇 ၁. ခွင့်ပြုမယ့် GROUP ID များ
ALLOWED_GROUPS = [
    '-1003606197582', 
    '-1003606197582'
]

# 👇 ၂. ခွင့်ပြုမယ့် USER ID များ
ALLOWED_USERS = [
    '1915369904',      # 1. Admin/Owner (မင်း ID)
    '6815134572',      # 2. သူငယ်ချင်း (၁) ID ထည့်ပါ
    'USER_ID_3_HERE',  # 3. သူငယ်ချင်း (၂) ID ထည့်ပါ
    'USER_ID_4_HERE',  # 4. သူငယ်ချင်း (၃) ID ထည့်ပါ
    'USER_ID_5_HERE'   # 5. သူငယ်ချင်း (၄) ID ထည့်ပါ
]
# ==========================================

# Token ဖတ်ခြင်း
try:
    with open('token.txt', 'r') as token_file:
        token = token_file.read().strip()
except FileNotFoundError:
    print("Error: token.txt file not found!")
    exit()

bot = TeleBot(token, parse_mode="HTML")

# ⛔ Permission စစ်ဆေးမယ့် Function
def is_allowed(message):
    chat_type = message.chat.type
    chat_id = str(message.chat.id)
    user_id = str(message.from_user.id)

    if chat_type == 'private':
        if user_id not in ALLOWED_USERS:
            bot.reply_to(message, "❌ <b>You are not authorized to use this bot in private!</b>", parse_mode="HTML")
            return False
            
    elif chat_type in ['group', 'supergroup']:
        if chat_id not in ALLOWED_GROUPS:
            bot.reply_to(message, "❌ <b>This group is not authorized.</b>", parse_mode="HTML")
            return False

    return True

@bot.message_handler(commands=["start"])
def start(message):
    if not is_allowed(message): return
    bot.reply_to(message,"<b>Bot Started!</b>\nUsage:\n/mt cc|mm|yy|cvc (Single)\n/mass (Bulk Check)")

# 🔥 /gfemin Command (Hit & Insu Only) 🔥
@bot.message_handler(commands=['gfemin'])
def send_hits_file(message):
    if not is_allowed(message): return

    file_name = "gfemin.txt"
    try:
        if os.path.exists(file_name):
            with open(file_name, "rb") as f:
                bot.send_document(
                    message.chat.id, 
                    f, 
                    caption="✅ <b>Here are your Hits & Insufficient Funds Cards</b>", 
                    parse_mode="HTML"
                )
        else:
            bot.reply_to(message, "No Hit or Insufficient Funds cards saved yet! ❌")
    except Exception as e:
        bot.reply_to(message, f"Error sending file: {e}")

# 🔥 Clear Command 🔥
@bot.message_handler(commands=['cleargfemin'])
def clear_hits_file(message):
    if not is_allowed(message): return
    if os.path.exists("gfemin.txt"):
        os.remove("gfemin.txt")
        bot.reply_to(message, "✅ File has been cleared.")
    else:
        bot.reply_to(message, "File is already empty.")

# ==========================================
# 🔥 MASS CHECKER LOGIC 🔥
# ==========================================
@bot.message_handler(commands=['mass'])
def mass_check(message):
    if not is_allowed(message): return
    
    # Threading သုံးမှ Bot မဟန်းမှာပါ
    t = threading.Thread(target=process_mass, args=(message,))
    t.start()
