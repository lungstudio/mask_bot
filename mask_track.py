import requests
import os
import time
from dotenv import load_dotenv
from os.path import join, dirname

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MASK_URLS = os.environ['MASK_URLS']
KEYWORDS_FOR_TRIGGER = os.environ['KEYWORDS_FOR_TRIGGER']
BOT_API_KEY = os.environ['BOT_API_KEY']
CHANNEL_NAME = os.environ['CHANNEL_NAME']
SLEEP_SEC = int(os.environ['SLEEP_SEC'])

def send_alert(url):
    msg = f"有口罩賣啦！{url}"
    tg_bot_url = f"https://api.telegram.org/bot{BOT_API_KEY}/sendMessage?chat_id={CHANNEL_NAME}&text={msg}"
    requests.get(tg_bot_url)

# main function for the cloud function to be executed
def mask_track(request):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3'
    }

    for url in MASK_URLS.split(','):
        r = requests.get(url, headers = headers)

        status = r.status_code
        is_mask_available = KEYWORDS_FOR_TRIGGER in r.text
        print(f"[mask_track] status: {status}, is_mask_available: {is_mask_available}, url: {url}")


        if status == 200 and is_mask_available:
            send_alert(url)

        time.sleep(SLEEP_SEC)

if __name__ == '__main__':
    mask_track(None)
