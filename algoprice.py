import json
import sys
import os
import requests

datafile = sys.argv[1]
asset1name = os.environ["ASSET1"]
asset2name = os.environ["ASSET2"]
asset1price = ""
asset2price = ""

with open(datafile, "r") as fd:
    data = json.load(fd)

for asset_ in data:
  if asset_['name'] == asset1name:
      asset1price = float(asset_['price'])
  if asset_['name'] == asset2name:
      asset2price = float(asset_['price'])

if not asset1price:
    raise IOError(f"Cannot find price of {asset1name}.")

if not asset2price:
    raise IOError(f"Cannot find price of {asset2name}.")

diff = round(asset2price / asset1price, 4)

headers = {'Content-type': 'application/json'}

url = os.environ['SLACK_WEBHOOK_URL']
print(f"URL: {url}")
if diff > 30:
    data = {"text":f"BANK/ALGO > 30.0 SELL ALGOS! price: {diff}"}
    res = requests.post(url, data=data, headers=headers)
elif diff < 21:
    data = {"text":f"BANK/ALGO < 21.0 BUY ALGOS! price {diff}"}
    res = requests.post(url, data=data, headers=headers)
else:
    data = {"text":f"BANK/ALGO = {diff} Nothing to do."}
    res = requests.post(url, data=data, headers=headers)

print(res)
    
