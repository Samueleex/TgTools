import telethon.sync
import telethon.errors.rpcerrorlist
import telethon.tl.functions.messages
import telethon.tl.functions.channels
import configparser
import csv
import time

RED = "\033[1;31m"
GREEN = "\033[1;32m"
CYAN = "\033[1;36m"
YELLOW = "\033[1;33m"


def read_config():
    config = configparser.RawConfigParser()
    config.read('config.data')
    return config['cred']['id'], config['cred']['hash'], config['cred']['phone']

def initialize_telegram_client(api_id, api_hash, phone):
    client = telethon.sync.TelegramClient(phone, api_id, api_hash)
    client.connect()
    if not client.is_user_authorized():
        client.send_code_request(phone)
        client.sign_in(phone, input(GREEN + '[+] Codice di verifica appena inviato: ' + YELLOW))
    return client

def select_group_to_scrape(groups):
    print('Scegli un gruppo:')
    for index, group in enumerate(groups):
        print(f"[{index}] - {group.title}")
    group_index = int(input("Enter a Number: "))
    return groups[group_index]

if __name__ == "__main__":
    print_custom_banner()
    api_id, api_hash, phone = read_config()
    telegram_client = initialize_telegram_client(api_id, api_hash, phone)
    dialogs = telegram_client(telethon.tl.functions.messages.GetDialogsRequest(offset_date=None, offset_id=0, offset_peer=telethon.tl.types.InputPeerEmpty(), limit=200, hash=0))
    groups = [dialog for dialog in dialogs.chats if hasattr(dialog, 'megagroup') and dialog.megagroup]
    target_group = select_group_to_scrape(groups)

    print(GREEN + '[+] Fetching Members ...')
    time.sleep(1)
    all_participants = telegram_client.iter_participants(target_group)

    print(GREEN + '[+] Saving in file ...')
    time.sleep(1)
    with open("members.csv", "w", encoding='UTF-8') as f:
        writer = csv.writer(f, delimiter=",", lineterminator="\n")
        writer.writerow(['username', 'user id', 'access hash', 'name', 'group', 'group id'])
        for user in all_participants:
            username = user.username or ""
            first_name = user.first_name or ""
            last_name = user.last_name or ""
            name = (first_name + ' ' + last_name).strip()
            writer.writerow([username, user.id, user.access_hash, name, target_group.title, target_group.id])

    print(GREEN + '[+] Members scraped successfully!')
