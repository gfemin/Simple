import requests

def send(cc, last, username, time_taken):
    ii = cc[:6]

    # Fixed amount (no random)
    fixed_amount = "𝟭"

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

    msg1 = f"""
𝐆𝐚𝐭𝐞𝐰𝐚𝐲 ➜ 𝐒𝐭𝐫𝐢𝐩𝐞 𝐠𝐚𝐭𝐞 {fixed_amount}$ 💰

𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞 ➜ {last}
𝐂𝐂 ➜ <code>{cc}</code>
𝐁𝐢𝐧 ➜ {ii}
𝐂𝐨𝐮𝐧𝐭𝐫𝐲 ➜ {do}
𝐁𝐚𝐧𝐤 ➜ {bank}
𝐅𝐥𝐚𝐠 ➜ {emj}

𝐂𝐡𝐞𝐜𝐤𝐞𝐝 𝐛𝐲 @{username}
𝐁𝐨𝐭 𝐛𝐲 @Rusisvirus
"""
    return msg1

