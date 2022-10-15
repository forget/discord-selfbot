from websocket import WebSocket
from json import loads, dumps
from os import _exit
from time import sleep
from random import randint

from threading import Thread
from requests import Response
from cloudscraper import create_scraper
from json.decoder import JSONDecodeError
from assets.settings import Config

class User(object):
    config = Config()
    def __init__(self, user_combo, uid) -> None:
        self.user_combo = user_combo
        self.uid = uid
        self.session = create_scraper(browser={"custom": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.49 Chrome/91.0.4472.164 Electron/13.6.6 Safari/537.36"})
        self.session.headers.update({"authorization": self.config.token})
        self.channel = None

    def __str__(self) -> str:
        return f"{self.user_combo} ({self.uid})"

    def get_channel(self, uid) -> str:
        payload = {
            "recipient_id": uid
        }

        r = self.session.post("https://canary.discord.com/api/v9/users/@me/channels", json=payload)

        return r.json()["id"]

    def send(self, message) -> Response:
        if self.channel:
            channel = self.channel

        else:
            channel = self.get_channel(self.uid)

        payload = {
            "content": message,
            "nonce": "".join([str(randint(0, 9)) for _ in range(19)]),
            "tts": False
        }

        r = self.session.post(f"https://canary.discord.com/api/v9/channels/{channel}/messages", json=payload)

        return r


class Monitor(object):
    config = Config()
    def __init__(self) -> None:
        self.session = create_scraper(browser={"custom": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.49 Chrome/91.0.4472.164 Electron/13.6.6 Safari/537.36"})
        self.session.headers.update({"authorization": self.config.token})
        self.ws = WebSocket()
        self.user = None
        self.running = True
        
        self.run()

    def listen(self) -> None:
        while self.running:
            result = self.ws.recv()

            try:
                data = loads(result)
            except JSONDecodeError:
                continue

            if data["t"] == "RELATIONSHIP_ADD" and data["d"]["type"] == 3:
                user_d = data["d"]["user"]
                user = User(f'{user_d["username"]}#{user_d["discriminator"]}', user_d["id"])

                print(f"\n[+] New add: {user}")

                if self.config.accept_friend_requests:
                    if self.config.delay_accept:
                        sleep(self.config.accept_delay)

                    r = self.accept(user)

                    if r.status_code == 204:
                        print(f"[+] Accepted {user}")

                    elif "captcha-required" in r.text:
                        print(f"[-] Failed to accept {user} | Captcha Required")
                        continue

                    else:
                        print(f"[-] Failed to accept {user} | {r.status_code} | {r.text}")
                        continue

                    if self.config.send_message:
                        if self.config.delay_message:
                            sleep(self.config.message_delay)

                        r = user.send(self.config.message)

                        if r.status_code == 200:
                            print(f"[+] Sent message to {user}")

                        elif "captcha-required" in r.text:
                            print(f"[-] Failed to send message to {user} | Captcha Required")

                        else:
                            print(f"[-] Failed to send message to {user} | {r.status_code} | {r.text}")

    def accept(self, user) -> Response:
        r = self.session.put(f"https://canary.discord.com/api/v9/users/@me/relationships/{user.uid}", json={})

        return r

    def stay_connected(self) -> None:
        payload = {
            "op": 1,
            "d": 6
        }

        while self.running:
            self.ws.send(dumps(payload))
            sleep(30)

    def login(self) -> None:
        self.ws.connect("wss://gateway.discord.gg/?encoding=json&v=9")
        self.ws.recv()

        payload = {
            "op": 2,
            "d": {
                "token": self.config.token,
                "capabilities": 1021,
                "properties": {
                    "os": "Windows",
                    "browser": "Chrome",
                    "device": "",
                    "system_locale": "en-US",
                    "browser_user_agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.49 Chrome/91.0.4472.164 Electron/13.6.6 Safari/537.36",
                    "browser_version": "91.0.4472.164",
                    "os_version": "10",
                    "referrer": "",
                    "referring_domain": "",
                    "referrer_current": "",
                    "referring_domain_current": "",
                    "release_channel": "stable",
                    "client_build_number": 150489,
                    "client_event_source": None
                },
                "presence": {
                    "status": "invisible",
                    "since": 0,
                    "activities": [],
                    "afk": False
                },
                "compress": False,
                "client_state": {
                    "guild_hashes": {},
                    "highest_last_message_id": "0",
                    "read_state_version": 0,
                    "user_guild_settings_version": -1,
                    "user_settings_version": -1,
                    "private_channels_version": "0"
                }
            }
        }

        self.ws.send(dumps(payload))

        result = self.ws.recv()

        try:
            data = loads(result)
        except JSONDecodeError:
            print("[-] Invalid token")
            self.ws.close()
            _exit(0)

        user_d = data["d"]["user"]
        self.user = User(f'{user_d["username"]}#{user_d["discriminator"]}', user_d["id"])

    def run(self) -> None:
        self.login()

        Thread(target=self.stay_connected).start()
        Thread(target=self.listen).start()

        print(f"[?] Auto-accept: {self.config.accept_friend_requests}")
        while (self.running):
            try:
                sleep(999)
            except KeyboardInterrupt:
                self.running = False
                self.ws.close()
                _exit(0)

if __name__ == "__main__":
    Monitor()
