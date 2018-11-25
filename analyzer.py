import requests

r = requests.get("https://rsbuddy.com/exchange/summary.json")

items = r.json()
items = list(items.items())

for uuid, item in items:
    sell = item['sell_average']
    buy = item['buy_average']

    margin = 0 if sell == 0 or buy == 0 else abs((buy - sell) / sell)
    margin *= 100 # For percentage

    item['margin'] = margin

    quantity = item['overall_quantity']
    average = item['overall_average']
    volume = 0 if average == 0 else quantity / average

    # Filter out low-cost items because they usually have unsatisfactory
    # profit
    score = 0 if average < 100 else margin * volume
    item['score'] = score

items = sorted(items, key=lambda a: a[1]['score'])

for uuid, item in items:
    print(item['name'], item['margin'], item['overall_quantity'])
