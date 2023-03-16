from twocaptcha import TwoCaptcha
from threading import Thread
from termcolor import colored
import websocket
import json
import cloudscraper
import time
from constants import (
    WEBSOCKET_URL,
    JOINRAIN_URL,
    HEADERS,
    AUTHS,
    SCRAPER
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
    def on_error(self, ws): print("error"),  time.sleep(5), self.connect()
    
    
    def ping(self, ws):
        while True:
            ws.send("3")
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
        #ws.send(f'42["time:requestSync",{{"clientTime":{time.time_ns()}}}]')
        time.sleep(1)
        ws.send('42["livefeed:subscribe"]')
        #ws.send(f'42["time:requestSync",{{"clientTime":{time.time_ns()}}}]')
        Thread(target=self.ping, args=[ws]).start()
        while 1:
            time.sleep(4)
            ws.send('42["cases:open",{"caseId":49,"openAmount":4,"fastAnimation":true}]')
            print("1")

        

    def on_message(self, ws, message):
        pass
        

Bot()