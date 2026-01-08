import requests

def send(cc, last, username, time_taken):
    ii = cc[:6]

    # Fixed amount
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

    # 🔥 FINAL CENTERED UI DESIGN 🔥
    msg1 = f"""<b>━━━━━━━━━━━━━</b>
   <b>Stripe Gateway ⚡️</b>
<b>━━━━━━━━━━━━━</b>
🔴 <b>Declined</b>
╰ {last}

💳 <code>{cc}</code>
🏦 {bank}
🌍 {do} {emj}
<b>━━━━━━━━━━━━━</b>
<b>Checked by @{username}</b>"""
    
    return msg1
