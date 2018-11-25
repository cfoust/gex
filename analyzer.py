import requests
import math
from tabulate import tabulate

r = requests.get("https://rsbuddy.com/exchange/summary.json")

items = r.json()
items = list(items.items())

for uuid, item in items:
    sell = item['sell_average']
    buy = item['buy_average']
    total_quantity = item['overall_quantity']
    buy_quantity = item['buy_quantity']
    sell_quantity = item['sell_quantity']
    average = item['overall_average']

    coin_margin = (buy - sell)
    percent_margin = 0 if sell == 0 or buy == 0 else abs(coin_margin / sell)
    percent_margin *= 100 # For percentage

    item['coin_margin'] = coin_margin
    item['percent_margin'] = percent_margin

    seller_ratio = 0 if buy_quantity == 0 else sell_quantity / buy_quantity

    # Make sure there are about equal buyers and sellers
    adjusted_ratio = pow(math.e, -1 * (pow(seller_ratio - 1, 2) / (2 * pow(1, 2))))
    desirable_volume = total_quantity / 8000 if total_quantity < 8000 else 1

    score = percent_margin * adjusted_ratio * desirable_volume

    # Filter out low-cost items because they usually have unsatisfactory
    # profit. Also, it's highly unlikely that margins greater than ~30%
    # are real.
    if average < 100 or coin_margin < 5 or percent_margin > 30:
        score = 0

    item['score'] = score

items = sorted(items, key=lambda a: a[1]['score'])
items = reversed(items)

items = [
    [
        item['name'][:20],
        item['buy_average'],
        item['sell_average'],
        round(item['percent_margin'], 2),
        item['coin_margin'],
        item['overall_quantity'],
        item['buy_quantity'],
        item['sell_quantity'],
    ]
    for uuid, item in items
]

headers = [
    'Name',
    'Buy',
    'Sell',
    '% Margin',
    'Gp Margin',
    'Overall V',
    'Buy V',
    'Sell V',
]

print(tabulate(items, headers=headers))

