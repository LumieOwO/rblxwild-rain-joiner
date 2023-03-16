import cloudscraper,twocaptcha

TWOCAPTCHA = ""
print(twocaptcha.TwoCaptcha(TWOCAPTCHA).balance())
AUTHS = [
    ""
]

WEBSOCKET_URL = "wss://rblxwild.com/socket.io/?EIO=4&transport=websocket"
JOINRAIN_URL  = "https://rblxwild.com/api/events/rain/join"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
}
SCRAPER = cloudscraper.create_scraper()