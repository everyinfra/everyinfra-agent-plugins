"""Use an IPFoxy proxy for your own requests and the EveryInfra data API for structured data.

Set two environment variables before you run this file:
  EVERYINFRA_API_KEY  your EveryInfra API key
  IPFOXY_PROXY        the connection string from the IPFoxy dashboard,
                      for example http://username:password@host:port
"""
import os

import requests

EVERYINFRA_API_KEY = os.environ["EVERYINFRA_API_KEY"]
IPFOXY_PROXY = os.environ["IPFOXY_PROXY"]
PROXIES = {"http": IPFOXY_PROXY, "https": IPFOXY_PROXY}

# 1. Your own request goes out through the IPFoxy exit IP.
exit_ip = requests.get("https://ipinfo.io/json", proxies=PROXIES, timeout=30).json()
print("Exit IP country:", exit_ip.get("country"))

# 2. The EveryInfra call goes direct. It does not need a proxy.
direct = requests.Session()
direct.trust_env = False  # ignore HTTP(S)_PROXY, so this call uses no proxy traffic
resp = direct.post(
    "https://api.everyinfra.com/api/v1/social",
    headers={"Authorization": f"Bearer {EVERYINFRA_API_KEY}"},
    json={
        "platform": "amazon",
        "action": "profile",
        "params": {"url": "https://www.amazon.com/dp/B0CYJDVT31"},
    },
    timeout=120,
)
resp.raise_for_status()
body = resp.json()
item = body["results"]
print(item["title"][:60], item["currency"], item["price"], item["rating"])
print("Charged USD:", body["billing"]["charged_usd"])
