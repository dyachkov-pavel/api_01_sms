import time
import requests
import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

vk_token = os.getenv('VK_TOKEN')
auth_token = os.getenv('AUTH_TOKEN')
account_sid = os.getenv('ACCOUNT_SID')
number_from = os.getenv('NUMBER_FROM')
number_to = os.getenv('NUMBER_TO')
client = Client(account_sid, auth_token)


def get_status(user_id):
    params = {
        'user_ids': user_id,
        'fields': 'online',
        'v': '5.92',
        'access_token': vk_token,
    }
    VK_URL = 'https://api.vk.com/method/'
    method = 'users.get'
    URL = VK_URL + method
    try:
        status = requests.post(URL, params=params).json()
        return status['response'][0]['online']
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:",errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
    except requests.exceptions.RequestException as err:
        print ("OOps: Something Else",err)


def sms_sender(sms_text):
    message = client.messages.create(
                                     body=sms_text,
                                     from_=number_from,
                                     to=number_to
                                    )
    return message.sid


if __name__ == '__main__':
    vk_id = input('Введите id ')
    while True:
        if get_status(vk_id) == 1:
            sms_sender(f'{vk_id} сейчас онлайн!')
            break
        time.sleep(5)
