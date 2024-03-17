import telethon.sync
import telethon.errors.rpcerrorlist
from telethon.tl.types import InputPeerUser
import configparser
import csv
import random
import time
import sys

RED = "\033[1;31m"
GREEN = "\033[1;32m"
CYAN = "\033[1;36m"
YELLOW = "\033[1;33m"
SLEEP_TIME = 30

class SMSBot:

    def __init__(self):
        self.api_id, self.api_hash, self.phone = self.read_config()
        self.client = self.initialize_telegram_client()

    def read_config(self):
        config = configparser.RawConfigParser()
        config.read('config.data')
        return config['cred']['id'], config['cred']['hash'], config['cred']['phone']

    def initialize_telegram_client(self):
        client = telethon.sync.TelegramClient(self.phone, self.api_id, self.api_hash)
        client.connect()
        if not client.is_user_authorized():
            client.send_code_request(self.phone)
            client.sign_in(self.phone, input(GREEN + '[+] Codice di verifica appena inviato: ' + YELLOW))
        return client

    def send_sms(self, input_file):
        users = self.read_users_from_csv(input_file)
        mode, message = self.get_user_input_for_sms()
        self.send_messages(users, mode, message)

    def read_users_from_csv(self, input_file):
        users = []
        with open(input_file, encoding='UTF-8') as f:
            rows = csv.reader(f, delimiter=",", lineterminator="\n")
            next(rows, None)
            for row in rows:
                user = {
                    'username': row[0],
                    'id': int(row[1]),
                    'access_hash': int(row[2]),
                    'name': row[3],
                }
                users.append(user)
        return users

    def get_user_input_for_sms(self):
        print(GREEN + "[1] Manda SMS da user ID\n[2] Manda username")
        mode = int(input(GREEN + "Input: " + RED))
        message = input(GREEN + "[+] Messaggio: " + YELLOW)
        return mode, message

    def send_messages(self, users, mode, message):
        for user in users:
            try:
                receiver = self.get_receiver(mode, user)
                print(GREEN + "[+] Sending Message to:", user['name'])
                self.client.send_message(receiver, message.format(user['name']))
                print(GREEN + "[+] Waiting {} seconds".format(SLEEP_TIME))
                time.sleep(SLEEP_TIME)
            except telethon.errors.rpcerrorlist.PeerFloodError:
                print(RED + "[!] Errori da Telegram. \n[!] Lo script ha smesso di funzionare. \n[!] Riprova più tardi.")
                break
            except Exception as e:
                print(RED + "[!] Errore:", e)
                print(RED + "[!] Sto riprovando ...")
                continue

    def get_receiver(self, mode, user):
        if mode == 1:
            return InputPeerUser(user['id'], user['access_hash'])
        elif mode == 2:
            if user['username']:
                return self.client.get_input_entity(user['username'])
            else:
                raise ValueError("Username non fornito")
        else:
            raise ValueError("Scelta invalida")


if __name__ == "__main__":
    sms_bot = SMSBot()
    input_file = sys.argv[1]
    sms_bot.send_sms(input_file)
