import requests
import os
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

AUTH_TOKEN = os.environ["AUTH_TOKEN"]
ACC_SID = os.environ["ACCOUNT_SID"]
PHONE_NUMBER = os.environ["NUMBER"]
TWILIO_NUM = os.environ["TWILIO_NUMBER"]
STOCK_ENDPOINT_API = os.environ["STOCKS_API_KEY"]
NEWS_ENDPOINT_API = os.environ["NEWS_API_KEY"]

stocks_parameters = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": STOCK_NAME,
    "datatype": "json",
    "apikey": STOCK_ENDPOINT_API
}

stocks_response = requests.get(url=STOCK_ENDPOINT, params=stocks_parameters)
stocks_data = stocks_response.json()['Time Series (Daily)']
data_list = [value for (key, value) in stocks_data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]

# the day before yesterday's data
day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]

# difference in the stock prices
difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)

percentage_difference = abs((difference/float(yesterday_closing_price)) * 100)
up_down = None

if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

if percentage_difference < 5:
    news_parameters = {
        "q": COMPANY_NAME,
        "apikey": NEWS_ENDPOINT_API
    }
    news_response = requests.get(url=NEWS_ENDPOINT, params=news_parameters)
    news_data = news_response.json()['articles']

    news_data_list = news_data[0:3]
    news_content = [f"{COMPANY_NAME}: {up_down}\nheadline: {data['title']}.\n " 
                    f"news_content:{data['description']}" for data in news_data_list]
    client = Client(ACC_SID, AUTH_TOKEN)
    for article in news_content:
        message = client.messages \
                    .create(
                         body=article,
                         from_=TWILIO_NUM,
                         to=PHONE_NUMBER
                     )

        print(message.sid)
