import requests
import json

PROXY_IP = "http://37.48.118.90:13042"


response = requests.get(
    "https://httpbin.org/ip", proxies={"http": PROXY_IP, "https": PROXY_IP}
)
print(response.text)
