import random

import requests


def check_rotating_ip():
    url = 'https://api.ipify.org'  # A website that returns your IP address

    # Send a request to the website
    response = requests.get(url,
                            proxies={"http": random.choice(["37.48.118.90:13042", "83.149.70.159:13042"])}
                            )

    # Check the IP address from which the request was made
    ip_address = response.text.strip()
    print(f"Current IP Address: {ip_address}")


if __name__ == '__main__':
    for i in range(10):
        check_rotating_ip()
