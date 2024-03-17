from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest
import configparser
import csv
import traceback
import time
import random
import sys 

RED = "\033[1;31m"
GREEN = "\033[1;32m"
CYAN = "\033[1;36m"


def read_config():
    config = configparser.RawConfigParser()
    config.read('config.data')
    return config['cred']['id'], config['cred']['hash'], config['cred']['phone']

def initialize_telegram_client(api_id, api_hash, phone):
    client = TelegramClient(phone, api_id, api_hash)
    client.connect()
    if not client.is_user_authorized():
        client.send_code_request(phone)
        client.sign_in(phone, input(GREEN + '[+] Enter the sent code: ' + RED))
    return client

def read_users_from_csv(filename):
    users = []
    with open(filename, encoding='UTF-8') as file:
        reader = csv.reader(file, delimiter=",", lineterminator="\n")
        next(reader, None)
        for row in reader:
            user = {
                'username': row[0],
                'id': int(row[1]),
                'access_hash': int(row[2]),
                'name': row[3],
            }
            users.append(user)
    return users

def select_target_group(groups):
    print(GREEN + '[+] Scegli un gruppo per aggiungere memberi: ' + RED)
    for index, group in enumerate(groups):
        print(f"{index}- {group.title}")
    group_index = int(input(GREEN + "Numero: " + RED))
    return groups[group_index]

def select_add_member_mode():
    print(GREEN + "[1] Aggiungi membri da user ID\n[2] Membri da username ")
    return int(input(GREEN + "Input: " + RED))

def add_members_to_group(client, users, target_group, mode):
    target_entity = InputPeerChannel(target_group.id, target_group.access_hash)
    n = 0
    for user in users:
        n += 1
        if n % 50 == 0:
            time.sleep(900)
        try:
            print(f"Adding {user['id']}")
            if mode == 1:
                if not user['username']:
                    continue
                user_to_add = client.get_input_entity(user['username'])
            elif mode == 2:
                user_to_add = InputPeerUser(user['id'], user['access_hash'])
            else:
                sys.exit(RED + "[!] Invalid Mode Selected. Please Try Again.")  # Correzione: Aggiunta di sys.exit()
            client(InviteToChannelRequest(target_entity, [user_to_add]))
            print(GREEN + "[+] Waiting for 60-180 sec ...")
            time.sleep(random.randrange(60, 180))
        except PeerFloodError:
            print(RED + "[!] Errori da Telegram. \n[!] Lo script ha smesso di funzionare. \n[!] Riprova più tardi.")
        except UserPrivacyRestrictedError:
            print(RED + "[!] Conflitto con le impostazioni di privacy!")
        except Exception as e:
            traceback.print_exc()
            print(RED + "[!] errore ", e)
            continue

if __name__ == "__main__":
    api_id, api_hash, phone = read_config()
    telegram_client = initialize_telegram_client(api_id, api_hash, phone)
    input_file = input(GREEN + "Enter the CSV file name: " + RED)
    users = read_users_from_csv(input_file)
    dialogs = telegram_client(GetDialogsRequest(offset_date=None, offset_id=0, offset_peer=InputPeerEmpty(), limit=200, hash=0))
    groups = [dialog for dialog in dialogs.chats if hasattr(dialog, 'megagroup') and dialog.megagroup]
    target_group = select_target_group(groups)
    mode = select_add_member_mode()
    add_members_to_group(telegram_client, users, target_group, mode)
