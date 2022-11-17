import json
import sys
import os
import requests
import shutil
import re

from datetime import datetime

get_date = datetime.now()
now = get_date.strftime("%Y-%m-%d %H:%M")
datafile = sys.argv[1]
asset1name = os.environ["ASSET1"]
asset2name = os.environ["ASSET2"]
asset1price = ""
asset2price = ""
notify = True
top_price = 35.0
bottom_price = 20.0

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

count_ = round(asset2price / asset1price, 4)

# Notification
if count_ > top_price:
    message = f"BANK/ALGO > {top_price} SELL ALGOS! price: {count_}"
    run = True
elif count_ < bottom_price:
    message = f"BANK/ALGO < {bottom_price} BUY ALGOS! price {count_}"
    run = True
else:
    print(f"BANK/ALGO = {count_} Nothing to do.")
    run = False

if run:
    url = os.environ['SLACK_URL']
    headers = {'Content-Type': "application/json"}
    slack_data = {"text": message}
    res = requests.post(url, data=json.dumps(slack_data), headers=headers)

    if res.status_code != 200:
        raise Exception(res.status_code, res.text)

# Page Update
if not os.path.exists('algo_bot/index.html'):
    shutil.copy('page/template.html', 'algo_bot/index.html')

with open('algo_bot/index.html', 'r') as fd:
    data = fd.readlines()

entry = f"['{now}', {count_}],\n"
for line_ in data:
    if "// Marker1" in line_:
        index_ = data.index(line_)

data.insert(index_, entry)

entry = f"['{now}', {asset2price}, {asset1price}],\n" 
for line_ in data:
    if "// Marker2" in line_:
        index_ = data.index(line_)

data.insert(index_, entry)


with open('algo_bot/index.html', "w") as fd:
    for line_ in data:
        line_ = "".join(line_)
        fd.write(line_)

        



