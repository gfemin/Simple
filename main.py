import time
import os  # os library ထပ်ထည့်ထားတယ်
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

# 👇 ၂. ခွင့်ပြုမယ့် USER ID များ (၄ ယောက်စာ နေရာလုပ်ပေးထားတယ်)
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

    # ၁. Private Chat ဖြစ်နေရင် -> User ID ကို စစ်မယ်
    if chat_type == 'private':
        if user_id not in ALLOWED_USERS:
            bot.reply_to(message, "❌ <b>You are not authorized to use this bot in private!</b>", parse_mode="HTML")
            return False
            
    # ၂. Group Chat ဖြစ်နေရင် -> Group ID ကို စစ်မယ်
    elif chat_type in ['group', 'supergroup']:
        if chat_id not in ALLOWED_GROUPS:
            bot.reply_to(message, "❌ <b>This group is not authorized.</b>", parse_mode="HTML")
            return False

    return True

@bot.message_handler(commands=["start"])
def start(message):
    if not is_allowed(message): return
    bot.reply_to(message,"/mt n|mm|yy|cvc (Visa/Mastercard)")

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

# 🔥 Clear Command (Optional - ဖျက်ချင်ရင်သုံးဖို့) 🔥
@bot.message_handler(commands=['cleargfemin'])
def clear_hits_file(message):
    if not is_allowed(message): return
    if os.path.exists("gfemin.txt"):
        os.remove("gfemin.txt")
        bot.reply_to(message, "✅ File has been cleared.")
    else:
        bot.reply_to(message, "File is already empty.")

@bot.message_handler(commands=['mt'])
def check_card(message):
    if not is_allowed(message): return

    try:
        try:
            cc = message.text.split('/mt', 1)[1].strip()
        except IndexError:
            bot.reply_to(message, "Please provide card details. Usage: /mt cc|mm|yy|cvv")
            return

        user_id = message.from_user.id
        username = message.from_user.username or "NoUsername"

        msg = bot.reply_to(message, "𝙲𝚑𝚎𝚌𝚔𝚒𝚗𝚐 𝚢𝚘𝚞𝚛 𝚌𝚊𝚛𝚍...")
        msg_id = msg.message_id  
        start_time = time.time()

        if not cc:
            bot.edit_message_text(
                chat_id=message.chat.id, message_id=msg_id,
                text="Invalid card format. Please use the correct format: `cc|mm|yy|cvv`",
                parse_mode="Markdown"
            )
            return

        try:
            last = str(Tele(cc))
        except:
            last = 'API Error'
        print(last)

        # Status Mapping
        # ဒီနေရာမှာ 'last' variable ကို မပြောင်းခင် Data ကို အရင်စစ်ပြီး သိမ်းမယ်
        
        save_status = None # သိမ်းမသိမ်း ဆုံးဖြတ်မယ့် variable

        if "Payment Successful" in last:
            last = '𝐓𝐫𝐚𝐧𝐬𝐚𝐜𝐭𝐢𝐨𝐧 𝐒𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥 🔥'
            save_status = "Charged ✅"
        elif "Your card does not support this type of purchase" in last:
            last = '𝐘𝐨𝐮𝐫 𝐜𝐚𝐫𝐝 𝐝𝐨𝐞𝐬 𝐧𝐨𝐭 𝐬𝐮𝐩𝐩𝐨𝐫𝐭 𝐭𝐡𝐢𝐬 𝐭𝐲𝐩𝐞 𝐨𝐟 𝐩𝐮𝐫𝐜𝐡𝐚𝐬𝐞'
        elif "security code is incorrect" in last or "security code is invalid" in last:
            last = '𝐬𝐞𝐜𝐮𝐫𝐢𝐭𝐲 𝐜𝐨𝐝𝐞 𝐢𝐬 𝐢𝐧𝐜𝐨𝐫𝐫𝐞𝐜𝐭/𝐢𝐧𝐯𝐚𝐥𝐢𝐝'
        elif "funds" in last:
            last = '𝐈𝐍𝐒𝐔𝐅𝐅𝐈𝐂𝐈𝐄𝐍𝐓_𝐅𝐔𝐍𝐃𝐒 🍃'
            save_status = "Low Funds 🍃"
        else:
            last = '𝐃𝐞𝐜𝐥𝐢𝐧𝐞𝐝'

        # 🔥 Saving Logic: Hit သို့မဟုတ် Funds ဖြစ်မှ gfemin.txt ထဲသိမ်းမယ် 🔥
        if save_status:
            with open("gfemin.txt", "a") as f:
                f.write(f"{cc} | {save_status}\n")

        time_taken = round(time.time() - start_time, 2)

        try:
            send_response = send(cc, last, username, time_taken)
        except Exception as e:
            send_response = f"Error generating response: {e}"

        print(send_response)

        try:
            bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=msg_id,
                text=send_response,
                parse_mode="HTML" 
            )
        except Exception as e:
            print(f"Error editing message: {e}")
            bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=msg_id,
                text="An error occurred while processing your request. Please try again later."
            )

    except Exception as e:
        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=msg_id,
            text="An error occurred while processing your request."
        )
        print(f"Error: {e}")

# Start the bot
print("Bot Started...")
bot.infinity_polling(timeout=25, long_polling_timeout=5)
