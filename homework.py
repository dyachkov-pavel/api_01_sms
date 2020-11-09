import time
import requests
import os
from dotenv import load_dotenv
from twilio.rest import Client
import logging

LOG_FORMAT = '%(levelname)s %(asctime)s - %(message)s'
logging.basicConfig(level=logging.ERROR,
                    format=LOG_FORMAT)
logger = logging.getLogger()

load_dotenv()

VK_TOKEN = os.getenv('VK_TOKEN')
VERSION = os.getenv('VERSION')
AUTH_TOKEN = os.getenv('AUTH_TOKEN')
ACCOUNT_SID = os.getenv('ACCOUNT_SID')
NUMBER_FROM = os.getenv('NUMBER_FROM')
NUMBER_TO = os.getenv('NUMBER_TO')
TWILIO_CLIENT = Client(ACCOUNT_SID, AUTH_TOKEN)


def get_status(user_id):
    params = {
        'user_ids': user_id,
        'fields': 'online',
        'v': VERSION,
        'access_token': VK_TOKEN,
    }
    vk_url = 'https://api.vk.com/method/'
    method = 'users.get'
    url = vk_url + method
    try:
        status = requests.post(url, params=params).json()
        return status['response'][0]['online']
    except requests.exceptions.HTTPError as errh:
        logger.error(f'Http Error: {errh}')
        raise errh
    except requests.exceptions.ConnectionError as errc:
        logger.error(f'Error Connecting: {errc}')
        raise errc
    except requests.exceptions.Timeout as errt:
        logger.error(f'Timeout Error: {errt}')
        raise errt
    except requests.exceptions.RequestException as err:
        logger.error(f'OOps: Something Else {err}')
        raise err
    except KeyError as errk:
        logger.error(f'OOps: Something Else {errk}')
        raise errk
    except IndexError as erri:
        logger.error(f'OOps: Something Else {erri}')
        raise erri


def sms_sender(sms_text):
    message = TWILIO_CLIENT.messages.create(
        body=sms_text,
        from_=NUMBER_FROM,
        to=NUMBER_TO
    )
    return message.sid


if __name__ == '__main__':
    vk_id = input('Введите id ')
    while True:
        if get_status(vk_id) == 1:
            sms_sender(f'{vk_id} сейчас онлайн!')
            break
        time.sleep(5)
