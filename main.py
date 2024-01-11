import requests
import datetime as dt
from twilio.rest import Client
import config
from twilio.base.exceptions import TwilioRestException


STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

AV_API_URL = "https://www.alphavantage.co/query"
NEWS_API_URL = "https://newsapi.org/v2/everything"

#API_KEY="O6SDHQUY6YPFWJAA"

#NEWS_KEY="44ec0cf826034511b55405586b50b2db"

MIN_CHANGE = 5

def check_price(name):


    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": name,
        "outputsize": "compact",
        "datatype": "json",
        "apikey": config.AV_API_KEY
    }
    response = requests.get(AV_API_URL, params=params)

    if response.status_code != 200:
        print(response.text)
        print("Make sure the AV_API_KEY is set properly in config.py.")

    return response.json()["Time Series (Daily)"]


def calculate_change(data):


    dates = list(data)
    yesterday_closing = float(data[dates[0]]["4. close"])
    day_before_closing = float(data[dates[1]]["4. close"])

    return (yesterday_closing - day_before_closing) / day_before_closing * 100


def get_news(name):
    """Takes a company name as a STR and returns a LIST of top related articles."""

    today = dt.datetime.today().strftime("%Y-%m-%d")
    params = {
        "q": f"{name}&",
        "from": f"{today}&",
        "sortBy": "popularity&",
        "apikey": config.NEWS_API_KEY
    }
    response = requests.get(NEWS_API_URL, params=params)
    if response.status_code != 200:
        print(response.text)
        print("Make sure the NEWS_API_KEY is set properly in config.py.")
        response.raise_for_status()
    # return articles only
    return response.json()["articles"]


def send_sms(sms_text):
    """Takes a message as STR and sends it as an SMS to the defined number."""
    # re-using the code from Day 35, with minor changes
    try:
        client = Client(config.TWILIO_SID, config.TWILIO_TOKEN)
        message = client.messages.create(body=sms_text, from_=config.TWILIO_NUMBER, to=config.TARGET_NUMBER)
    except TwilioRestException as ex:
        # a generic error message that will get displayed with each failed attempt
        print(ex)
        print("Make sure the TWILIO_SID, TWILIO_TOKEN, TWILIO_NUMBER and TARGET_NUMBER are set properly in config.py.")
    else:
        print(message.status)


daily_data = check_price(STOCK_NAME)


change = calculate_change(daily_data)

n
if abs(change) >= MIN_CHANGE:
    message_head = f"{STOCK_NAME}: "
    if change >= MIN_CHANGE:
        message_head += "🔺"
    else:
        message_head += "🔻"
    # include the percentage
    message_head += f"{abs(round(change, 1))}%\n"

    # get news data for the company name
    news_data = get_news(COMPANY_NAME)
    # send a message with the top three articles
    for i in range(3):
        # clear the content before each iteration
        message_content = ""
        # add the titles and descriptions
        message_content += f"Headline: {news_data[i]['title']}\n"
        message_content += f"Brief: {news_data[i]['description'].strip('Summary List Placement')}"
        # send the sms
        send_sms(message_head + message_content)









