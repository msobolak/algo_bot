import json
import sys
import os

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

print(asset2price / asset1price)
