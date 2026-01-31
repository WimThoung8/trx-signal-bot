import telegram
from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram import Update
import requests
import time
import hashlib
import random
import string

BOT_TOKEN = "8409859323:AAE3roaqVk3ZGMfokA_KXYJRwa5fklrMa9o"
API_URL = "https://api.bigwinqaz.com/api/webapi/GetTRXGameIssue"

def generate_signature(random_str, timestamp):
    s = random_str + str(timestamp)
    return hashlib.md5(s.encode()).hexdigest().upper()

def fetch_trx_issue():
    timestamp = int(time.time() * 1000)
    random_str = ''.join(random.choices(string.digits + string.ascii_lowercase, k=32))
    signature = generate_signature(random_str, timestamp)

    payload = {
        "typeId": 13,
        "language": 7,
        "random": random_str,
        "timestamp": timestamp,
        "signature": signature
    }

    headers = {
        "Content-Type": "application/json",
        "Origin": "https://www.777bigwingame.app",
        "Referer": "https://www.777bigwingame.app/"
    }

    try:
        res = requests.post(API_URL, json=payload, headers=headers, timeout=10)
        return res.json()["data"]
    except:
        return None

def get_bigsmall(number):
    try:
        n = int(number)
        return "BIG 🟢" if n >= 5 else "SMALL 🔴"
    except:
        return "❓"

def send_signal(context: CallbackContext):
    data = fetch_trx_issue()
    if data is None:
        return

    predraw = data["predraw"]
    settled = data["settled"]

    msg = f"""
🎯 *TRX SIGNAL (1-Minute)*  
━━━━━━━━━━━━━━━  
🕒 *Period:* `{predraw['issueNumber']}`  
🎲 *Result:* {get_bigsmall(settled['number'])}  
🔢 *Number:* {settled['number']}  
━━━━━━━━━━━━━━━  
⚡ Auto Signal Bot  
"""

    context.bot.send_message(
        chat_id=context.job.context,
        text=msg,
        parse_mode="Markdown"
    )

def start(update: Update, context: CallbackContext):
    update.message.reply_text("TRX Signal Bot Activated ✔")
    chat_id = update.message.chat_id
    context.job_queue.run_repeating(send_signal, 60, first=3, context=chat_id)

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
