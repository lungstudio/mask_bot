import requests
import os
from dotenv import load_dotenv
from os.path import join, dirname

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MASK_URL = os.environ['MASK_URL']
KEYWORDS_FOR_TRIGGER = os.environ['KEYWORDS_FOR_TRIGGER']
BOT_API_KEY = os.environ['BOT_API_KEY']
CHANNEL_NAME = os.environ['CHANNEL_NAME']

def send_alert():
    msg = f"有口罩賣啦！{MASK_URL}"
    tg_bot_url = f"https://api.telegram.org/bot{BOT_API_KEY}/sendMessage?chat_id={CHANNEL_NAME}&text={msg}"
    requests.get(tg_bot_url)

# main function for the cloud function to be executed
def mask_track(request):
    r = requests.get(MASK_URL)

    status = r.status_code
    is_mask_available = KEYWORDS_FOR_TRIGGER not in r.text
    print(f"[mask_track] status: {status}, is_mask_available: {is_mask_available}")

    if status == 200 and is_mask_available:
        send_alert()

if __name__ == '__main__':
    mask_track(None)
