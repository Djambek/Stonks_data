from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta, MO 
import requests

def get_stock_data_true(ticker: str, period: str):
    now,past = get_date(period=period)
    now_price, past_price = request(ticker=ticker, now=now, past=past)
    return get_percentage(now_price=now_price, past_price=past_price)
def get_date(period):
    now = datetime.now() - timedelta(1) # изменил
    y = period.find("y") if period.count("y") else -1
    m = period.find("m") if period.count("m") else -1
    d = period.find("d") if period.count("d") else -1

    year = period[:y] if y>0 else 0
    month = period[y+1:m] if m>0 else 0
    if m == -1 and d>0:
        day = period[y+1:d] if d > 0 else 0 
    else:
        day = period[m+1:d] if d > 0 else 0 
    # print(year, month, day) 
    if now.weekday() == 6:
        now -= timedelta(3)
    if now.weekday() == 5:
        now -= timedelta(2)
    past = now+relativedelta(years =- int(year), months =- int(month), days =- int(day))
    if past.weekday() == 6:
        past += timedelta(1)
    if past.weekday() == 5:
        past += timedelta(2)

    return (str(now).split()[0], str(past).split()[0])

def request(ticker, now, past):
    headers = {
    'Content-Type': 'application/json'
    }   
    # print(now)
    requestResponse = requests.get("https://api.tiingo.com/tiingo/daily/{}/prices?startDate={}&endDate={}&token=15b862c10e24d47b6f1a08fa5d1fe578f605e73f".format(ticker, now, now), headers=headers)
    # print(requestResponse.json())
    now_price = int(requestResponse.json()[0]["adjHigh"])+ int(requestResponse.json()[0]["adjClose"]) / 2

    requestResponse = requests.get("https://api.tiingo.com/tiingo/daily/{}/prices?startDate={}&endDate={}&token=15b862c10e24d47b6f1a08fa5d1fe578f605e73f".format(ticker, past, past), headers=headers)
    past_price = int(requestResponse.json()[0]["adjHigh"])+ int(requestResponse.json()[0]["adjClose"]) / 2
    return (now_price, past_price)

def get_percentage(now_price, past_price):
    # print(now_price, past_price)
    if now_price > past_price:
        return "+" + str(round((now_price/past_price)*100, 2)) + "%"
    if now_price < past_price:
        return "-" + str(round((past_price/now_price*100), 2)) + "%"
