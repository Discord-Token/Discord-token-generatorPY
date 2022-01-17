import os
from os import system
import httpx
from base64 import b64encode
from colorama import init, Fore, Style
from random import choice
from threading import RLock, Thread
from time import time, sleep
import websocket
import base64
from concurrent.futures import ThreadPoolExecutor
import json
import random
init(convert=True)
folder=r"Data/Avatars"
captchaApi = "anti-captcha.com" # 2captcha.com anti-captcha.com capmonster.cloud (use anti captcha, other services are patched)

password = "Oxi$tinks"

captchaKey = "KEY"
genStartTime = time()
generatedTokens = 0
failedTokens = 0
erroredTokens = 0
solved = 0
class SynchronizedEcho(object):
    print_lock = RLock()

    def __init__(self, global_lock=True):
        if not global_lock:
            self.print_lock = RLock()

    def __call__(self, msg):
        with self.print_lock:
            print(msg)

s_print = SynchronizedEcho()
def username():
    usernames = open("usernames.txt", encoding="cp437", errors='ignore').read().splitlines()
    return random.choice(usernames)

def generateToken():
    global generatedTokens
    global failedTokens
    global solved
    global erroredTokens
    global regReq
    try:
        system(f"title Token Generator V1ㅣ{round(generatedTokens / ((time() - genStartTime) / 60))}/mㅣSuccess {generatedTokens}ㅣFailed {failedTokens}ㅣError {erroredTokens} ㅣ Solved {solved}")

        proxy = ""
        with open("Proxies.txt", "r") as f:
            proxy = "http://" + choice(f.readlines()).strip()

        with httpx.Client(cookies={"locale": "en-US"}, headers={"Accept": "*/*", "Accept-Language": "en-US", "Connection": "keep-alive", "Content-Type": "application/json", "DNT": "1", "Host": "discord.com", "Referer": "https://discord.com/", "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "same-origin", "TE": "trailers", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0", "X-Track": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRmlyZWZveCIsImRldmljZSI6IiIsInN5c3RlbV9sb2NhbGUiOiJlbi1VUyIsImJyb3dzZXJfdXNlcl9hZ2VudCI6Ik1vemlsbGEvNS4wIChXaW5kb3dzIE5UIDEwLjA7IFdpbjY0OyB4NjQ7IHJ2Ojk0LjApIEdlY2tvLzIwMTAwMTAxIEZpcmVmb3gvOTQuMCIsImJyb3dzZXJfdmVyc2lvbiI6Ijk0LjAiLCJvc192ZXJzaW9uIjoiMTAiLCJyZWZlcnJlciI6IiIsInJlZmVycmluZ19kb21haW4iOiIiLCJyZWZlcnJlcl9jdXJyZW50IjoiIiwicmVmZXJyaW5nX2RvbWFpbl9jdXJyZW50IjoiIiwicmVsZWFzZV9jaGFubmVsIjoic3RhYmxlIiwiY2xpZW50X2J1aWxkX251bWJlciI6OTk5OSwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbH0="}, proxies=proxy) as client:
            client.headers["X-Fingerprint"] = client.get("https://discord.com/api/v9/experiments", timeout=30).json().get("fingerprint")
            client.headers["Origin"] = "https://discord.com"
            taskId = ""
            taskId = httpx.post(f"https://api.{captchaApi}/createTask", json={"clientKey": captchaKey, "task": {"type": "HCaptchaTaskProxyless", "websiteURL": "https://discord.com/", "websiteKey": "f5561ba9-8f1e-40ca-9b5b-a0b3f719ef34", "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0"}}, timeout=30).json()
            if taskId.get("errorId") > 0:
                s_print(f"{Fore.RED}{Style.BRIGHT}[-] createTask - {taskId.get('errorDescription')}!{Style.RESET_ALL}")
                erroredTokens += 0
                return generateToken()
            taskId = taskId.get("taskId")


            captchaTries = 0
            solvedCaptcha = None
            while not solvedCaptcha:
                    captchaData = httpx.post(f"https://api.{captchaApi}/getTaskResult", json={"clientKey": captchaKey, "taskId": taskId}, timeout=30).json()
                    if captchaData.get("status") == "ready":
                        solvedCaptcha = captchaData.get("solution").get("gRecaptchaResponse")
                        solved += 1
							


                        regReq = client.post("https://discord.com/api/v9/auth/register", json={"consent": True, "fingerprint": client.headers["X-Fingerprint"], "username": username(), "captcha_key": solvedCaptcha}, timeout=30)
                        token = regReq.json().get("token")

                        
                        client.headers["Authorization"] = token
                        del client.headers["Origin"]
                        client.headers["Referer"] = "https://discord.com/channels/@me"
                        client.headers["X-Debug-Options"] = "bugReporterEnabled"
                        del client.headers["X-Track"]
                        client.headers["X-Super-Properties"] = "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRmlyZWZveCIsImRldmljZSI6IiIsInN5c3RlbV9sb2NhbGUiOiJlbi1VUyIsImJyb3dzZXJfdXNlcl9hZ2VudCI6Ik1vemlsbGEvNS4wIChXaW5kb3dzIE5UIDEwLjA7IFdpbjY0OyB4NjQ7IHJ2Ojk1LjApIEdlY2tvLzIwMTAwMTAxIEZpcmVmb3gvOTUuMCIsImJyb3dzZXJfdmVyc2lvbiI6Ijk1LjAiLCJvc192ZXJzaW9uIjoiMTAiLCJyZWZlcnJlciI6IiIsInJlZmVycmluZ19kb21haW4iOiIiLCJyZWZlcnJlcl9jdXJyZW50IjoiIiwicmVmZXJyaW5nX2RvbWFpbl9jdXJyZW50IjoiIiwicmVsZWFzZV9jaGFubmVsIjoic3RhYmxlIiwiY2xpZW50X2J1aWxkX251bWJlciI6MTA4OTI0LCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ=="



                        email = "".join(choice("abcdefghijklmnopqrstuvwxyz") for i in range(10))
                        email += "@OxiHasGithub.com"
                        a=random.choice(os.listdir(folder))
                        avatar = folder+'\\'+a
                        imgg = base64.b64encode(open(f"{avatar}", "rb").read()).decode('ascii')
                        userData = client.patch("https://discord.com/api/v9/users/@me", json={"email": email, "password": password, "date_of_birth": "2000-01-01", "avatar": f"data:image/png;base64,{imgg}"}, timeout=30)
                        if userData.status_code == 403:
                            with open("Locked_tokens.txt", "a")as shittoken:
                                shittoken.write(f"{token}\n")
                            failedTokens += 1
                            return generateToken()

                        emailData = ""
                        ws = websocket.WebSocket();ws.connect('wss://gateway.discord.gg/?v=6&encoding=json');response=ws.recv();event=json.loads(response);auth={'op':2,'d':{'token':token,'capabilities':61,'properties':{'os':'Windows','browser':'Chrome','device':'','system_locale':'en-GB','browser_user_agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36','browser_version':'90.0.4430.212','os_version':'10','referrer':'','referring_domain':'','referrer_current':'','referring_domain_current':'','release_channel':'stable','client_build_number':'85108','client_event_source':'null'},'presence':{'status':'dnd','since':0,'activities':[],'afk':False},'compress':False,'client_state':{'guild_hashes':{},'highest_last_message_id':'0','read_state_version':0,'user_guild_settings_version':-1}}};ws.send(json.dumps(auth));ws.close()
                        while len(emailData) == 0:
                            emailData = httpx.get("http://104.128.232.196:12345/api/getInbox?email=" + email).text

                        emailToken = httpx.get("https://click.discord.com/ls/click?upn=" + emailData, headers={"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8", "Accept-Language": "en-US", "Connection": "keep-alive", "DNT": "1", "Host": "click.discord.com", "Sec-Fetch-Dest": "document", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-Site": "none", "Sec-Fetch-User": "?1", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0"}).headers.get("location").split("=")[1]

                        client.headers["Authorization"] = "undefined"
                        client.headers["Referer"] = "https://discord.com/verify"
									
                        emailData = client.post("https://discord.com/api/v9/auth/verify", json={"token": emailToken, "captcha_key": None}, timeout=30)
                        if emailData.status_code == 400:
                            s_print(f"{Fore.RED}{Style.BRIGHT}[-] Captcha on email verify, retrying!")
                            emailData = client.post("https://discord.com/api/v9/auth/verify", json={"token": emailToken, "captcha_key": None}, timeout=30)
                            if emailData.status_code == 400:
                                with open("Unverified_tokens.txt", "a")as shittoken1:
                                    shittoken1.write(f"{token}\n")
                                    failedTokens += 1
                                    return generateToken()
                            else:
                                print(f"Succesfully passed captcha on 2nd try!")
                                pass

                        userData = userData.json()
                        s_print(f"{Fore.GREEN}{Style.BRIGHT}[+] Token generated - {emailData.json().get('token')} {Style.RESET_ALL}")

                        generatedTokens += 1

                        with open("Tokens.txt", "a") as f:
                            f.write(f"{email}:{password}:{emailData.json().get('token')}\n")
                            f.close()
                        with open("Tokens_unformat.txt", "a") as g:
                            g.write(f"{emailData.json().get('token')}\n")
                            g.close()
                            
    except Exception as e:
        s_print(f"{Fore.YELLOW}{Style.BRIGHT}[-] Error: {e}{Style.RESET_ALL}")
        s_print(regReq.text)
        erroredTokens += 1
    generateToken()
if __name__ == "__main__":
    system("cls")
    print("Token Generator V1.2\n")
    threadAmount = input(f"{Fore.BLUE}{Style.BRIGHT}[?] Number of threads -> {Style.RESET_ALL}")
    threadAmount = 1 if threadAmount == "" else int(threadAmount)
    system("cls")
    threads = []
    with ThreadPoolExecutor(max_workers=threadAmount) as ex : 
        
        for x in range(threadAmount):
            
            ex.submit(generateToken)
