from twocaptcha import TwoCaptcha
from threading import Thread
from termcolor import colored
import websocket
import requests
import json
import time
import random
from constants import (
    WEBSOCKET_URL,
    JOINRAIN_URL,
    HEADERS,
    AUTHS,
    TWOCAPTCHA
)

def x(text, color="green"):
    print(colored(text, color, attrs=["bold"]))


class Bot(websocket.WebSocketApp):
    def __init__(self):
        self.join_limit = 5
        self.rain_state = "events:rain:setPot"
        self.connect()
    
    
    def connect(self):
        super().__init__(
            url=WEBSOCKET_URL,
            on_open=self.on_open,
            on_close=self.on_close,
            on_error=self.on_error,
            on_message=self.on_message,
            header=HEADERS
        )
        
        super().run_forever()
    
    
    def on_close(self, ws): print("closed"), time.sleep(5), self.connect()
    def on_error(self, ws,error): print(error),  time.sleep(5), self.connect()
    
    
    def ping(self, ws):
        while True:
            try:
                ws.send("3")
            except:
                break
            time.sleep(8)
            
            #for _ in range(6):
            #    ws.send(f'42["time:requestSync",{{"clientTime":{time.time_ns()}}}]')
            #    time.sleep(1)            
            
            
    def on_open(self, ws):
        ws.send('40')
        #ws.send(f'42["time:requestSync",{{"clientTime":{time.time_ns()}}}]')
        time.sleep(1)
        ws.send(f'42["authentication",{{"authToken":"{AUTHS[0]}","clientTime":{time.time_ns()}}}]')
        #ws.send(f'42["time:requestSync",{{"clientTime":{time.time_ns()}}}]')
        time.sleep(1)
        ws.send('42["chat:subscribe",{"channel":"EN"}]')
        ws.send('42["crash:subscribe"]')
        #ws.send(f'42["time:requestSync",{{"clientTime":{time.time_ns()}}}]')
        time.sleep(1)
        ws.send('42["livefeed:subscribe"]')
        #ws.send(f'42["time:requestSync",{{"clientTime":{time.time_ns()}}}]')
        Thread(target=self.ping, args=[ws]).start()
        Thread(target=self.crash_join, args=[ws]).start()

    def crash_join(self,ws):
        while True:
            ws.send('42["crash:bet",{"betAmount":2,"autoCashout":1.01}]')
            time.sleep(random.randint(7234,14434))
                
    def on_message(self, ws, message):
        try:
            if message == "2":
                return
            
            data = json.loads(message[2:])
            if data[0] != self.rain_state:
                return

            if self.join_limit <= 0:
                self.join_limit = 5
                x(f"not joining current rain to prevent ban", "magenta")
                ws.send('42["cases:open",{"caseId":49,"openAmount":1,"fastAnimation":true}]')
                return
            self.join_limit -= 1

            potId = data[1]["newPot"]["id"]
            x(f"new rain! id: {potId}", "cyan")

            time.sleep(1678)

            x("rain started!", "cyan")

            for auth in AUTHS:
                Thread(target=self.join_rain, args=[auth, potId]).start()
        except:
            pass

    def join_rain(self, auth, potId):
        solver = TwoCaptcha(TWOCAPTCHA)
        
        captcha = solver.hcaptcha(
            "30a8dcf5-481e-40d1-88de-51ad22aa8e97",
            "rblxwild.com"
        )
        
        data = requests.post(JOINRAIN_URL, headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
            "content-type": "application/json",
            "authorization": auth
        }, data = json.dumps({
            "captchaToken": captcha["code"],
            "i1oveu": True,
            "potId": potId   
        }))
        
        solver.report(captcha["captchaId"], False)
        x(data.content)
        

Bot()