import telethon.sync
import telethon.errors.rpcerrorlist
import telethon.tl.types
import telethon.tl.functions.messages
import telethon.tl.functions.channels
import configparser
import csv
import time
import random
import traceback
import sys

API_ID = ""  # ID API Telegram
API_HASH = ""  # hash API (32 caratteri)
PHONE_NUMBER = ""  # numero di telefono con il prefisso internazionale


def read_config():
    config = configparser.RawConfigParser()
    config.read('config.data')
    return config['cred']['id'], config['cred']['hash'], config['cred']['phone']

def initialize_telegram_client(api_id, api_hash, phone):
    client = telethon.sync.TelegramClient(phone, api_id, api_hash)
    client.connect()
    if not client.is_user_authorized():
        client.send_code_request(phone)
        client.sign_in(phone, input('Codice inviato: '))
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
    print('Scegli un gruppo: ')
    for index, group in enumerate(groups):
        print(f"{index}- {group.title}")
    group_index = int(input("Enter a Number: "))
    return groups[group_index]

def select_add_member_mode():
    print("[1] Aggiungi membri da user ID\n[2] Membri per username ")
    return int(input("Input: "))

if __name__ == "__main__":
    print_custom_banner()
    api_id, api_hash, phone = read_config()
    telegram_client = initialize_telegram_client(api_id, api_hash, phone)
    input_file = input("Enter the CSV file name: ")
    users = read_users_from_csv(input_file)
    dialogs = telegram_client(telethon.tl.functions.messages.GetDialogsRequest(offset_date=None, offset_id=0, offset_peer=telethon.tl.types.InputPeerEmpty(), limit=200, hash=0))
    groups = [dialog for dialog in dialogs.chats if hasattr(dialog, 'megagroup') and dialog.megagroup]
    target_group = select_target_group(groups)
    mode = select_add_member_mode()
    target_entity = telethon.tl.types.InputPeerChannel(target_group.id, target_group.access_hash)

    n = 0
    for user in users:
        n += 1
        if n % 80 == 0:
            time.sleep(60)
        try:
            print(f"Adding {user['id']}")
            if mode == 1:
                if not user['username']:
                    continue
                user_to_add = telegram_client.get_input_entity(user['username'])
            elif mode == 2:
                user_to_add = telethon.tl.types.InputPeerUser(user['id'], user['access_hash'])
            else:
                sys.exit("Scelta invalida!")
            telegram_client(telethon.tl.functions.channels.InviteToChannelRequest(target_entity, [user_to_add]))
            print("Waiting for 60-180 Seconds ...")
            time.sleep(random.randrange(0, 5))
        except telethon.errors.rpcerrorlist.PeerFloodError:
            print("Errori da Telegram. Lo script ha smesso di funzionare. Riprova più tardi.")
            time.sleep(100)
        except telethon.errors.rpcerrorlist.UserPrivacyRestrictedError:
            print("Conflitto con le impostazioni di privacy!")
            time.sleep(random.randrange(0, 5))
        except Exception as e:
            traceback.print_exc()
            print("Unexpected Error! ", e)
            continue
