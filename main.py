import time
from telebot import TeleBot, types
from gatet import Tele
from hit_sender import send  

admin_name = "@Rusisvirus"

# ==========================================
# 👇 ဒီနေရာမှာ ခွင့်ပြုမယ့် GROUP ID တွေကို ထည့်ပါ
# Group ID တွေက များသောအားဖြင့် -100 နဲ့ စပါတယ်
ALLOWED_GROUPS = [
    '-1003606197582',   # Group 1 ID
    '-1003606197582'    # Group 2 ID
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

# ⛔ Private Chat တွေမှာ သုံးမရအောင် တားမယ့် Function
def is_allowed(message):
    # 1. Private Chat ဖြစ်နေရင် ငြင်းမယ်
    if message.chat.type == 'private':
        bot.reply_to(message, "❌ <b>This bot only works in authorized groups!</b>", parse_mode="HTML")
        return False
    
    # 2. Group ID က list ထဲမှာ မပါရင် ငြင်းမယ်
    if str(message.chat.id) not in ALLOWED_GROUPS:
        bot.reply_to(message, "❌ <b>This group is not authorized.</b>", parse_mode="HTML")
        return False
        
    return True

@bot.message_handler(commands=["start"])
def start(message):
    # Permission စစ်မယ်
    if not is_allowed(message): return
    
    bot.reply_to(message,"/mt n|mm|yy|cvc (Visa/Mastercard)")

@bot.message_handler(commands=['mt'])
def check_card(message):
    # Permission စစ်မယ်
    if not is_allowed(message): return

    try:
        # User input မှားရင် error မတက်အောင် try catch ခံထားတာ
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
        if "Payment Successful" in last:
            last = '𝐓𝐫𝐚𝐧𝐬𝐚𝐜𝐭𝐢𝐨𝐧 𝐒𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥 🔥'
        elif "Your card does not support this type of purchase" in last:
            last = '𝐘𝐨𝐮𝐫 𝐜𝐚𝐫𝐝 𝐝𝐨𝐞𝐬 𝐧𝐨𝐭 𝐬𝐮𝐩𝐩𝐨𝐫𝐭 𝐭𝐡𝐢𝐬 𝐭𝐲𝐩𝐞 𝐨𝐟 𝐩𝐮𝐫𝐜𝐡𝐚𝐬𝐞'
        elif "security code is incorrect" in last or "security code is invalid" in last:
            last = '𝐬𝐞𝐜𝐮𝐫𝐢𝐭𝐲 𝐜𝐨𝐝𝐞 𝐢𝐬 𝐢𝐧𝐜𝐨𝐫𝐫𝐞𝐜𝐭/𝐢𝐧𝐯𝐚𝐥𝐢𝐝'
        elif "funds" in last:
            last = '𝐈𝐍𝐒𝐔𝐅𝐅𝐈𝐂𝐈𝐄𝐍𝐓_𝐅𝐔𝐍𝐃𝐒 🍃'
        else:
            last = '𝐃𝐞𝐜𝐥𝐢𝐧𝐞𝐝'

        time_taken = round(time.time() - start_time, 2)

        # hit_sender ကနေ message format ယူမယ်
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
