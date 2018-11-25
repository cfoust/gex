import requests

r = requests.get("https://rsbuddy.com/exchange/summary.json")

items = r.json()
items = list(items.items())

for uuid, item in items:
    sell = item['sell_average']
    buy = item['buy_average']

    coin_margin = (buy - sell)
    percent_margin = 0 if sell == 0 or buy == 0 else abs(coin_margin / sell)
    percent_margin *= 100 # For percentage

    item['margin'] = percent_margin

    quantity = item['overall_quantity']
    average = item['overall_average']
    volume = 0 if average == 0 else quantity / average

    score = percent_margin * volume

    # Filter out low-cost items because they usually have unsatisfactory
    # profit
    if average < 100 or coin_margin < 2:
        score = 0

    item['score'] = score

items = sorted(items, key=lambda a: a[1]['score'])

for uuid, item in items:
    output = [
        item['name'],
        item['margin'],
        item['buy_average'],
        item['sell_average'],
        item['overall_quantity']
    ]
    print('\t'.join([str(x) for x in output]))
