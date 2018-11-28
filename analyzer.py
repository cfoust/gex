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

    coin_margin = abs(buy - sell)
    percent_margin = 0 if sell == 0 or buy == 0 else coin_margin / sell
    percent_margin *= 100 # For percentage

    item['coin_margin'] = coin_margin
    item['percent_margin'] = percent_margin

    market_cap = total_quantity * average
    seller_ratio = 0 if buy_quantity == 0 else sell_quantity / buy_quantity

    # Make sure there are about equal buyers and sellers
    adjusted_ratio = pow(math.e, -1 * (pow(seller_ratio - 1.2, 2) / (2 * pow(0.5, 2))))

    score = percent_margin * total_quantity * adjusted_ratio

    # Filter out low-cost items because they usually have unsatisfactory
    # profit. Also, it's highly unlikely that margins greater than ~30%
    # are real.
    if average < 100 or coin_margin < 5 or percent_margin > 25:
        score = 0

    item['score'] = score

items = [(uuid, item) for uuid, item in items if item['overall_average'] < 1100000000]
items = sorted(items, key=lambda a: a[1]['score'])
items = reversed(items)

def round_volume(volume):
    return str(round(volume / 1000, 1)) + 'k'

items = [
    [
        item['name'][:20],
        item['buy_average'],
        item['sell_average'],
        round(item['percent_margin'], 2),
        item['coin_margin'],
        round_volume(item['overall_quantity']),
        round_volume(item['buy_quantity']),
        round_volume(item['sell_quantity']),
        # round(item['score'], 2),
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
    'Score',
]

print(tabulate(items, headers=headers))

