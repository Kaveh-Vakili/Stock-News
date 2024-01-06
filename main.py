import requests

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

API_KEY="O6SDHQUY6YPFWJAA"

stock_parameters={
    "function": "TIME_SERIES_DAILY",
    "symbol":STOCK_NAME,
    "apikey":API_KEY,
}




response=requests.get(STOCK_ENDPOINT,params=stock_parameters)



data=response.json()["Time Series (Daily)"]

data_list=  [value for(key,value)  in data.items()]


yesterday_Data=data_list[0]

yesterday_Closing_Price=yesterday_Data["4. close"]

two_days_Ago_Data=data_list[1]

two_days_Ago_Price=two_days_Ago_Data["4. close"]

difference=abs(float(yesterday_Closing_Price)-float(two_days_Ago_Price))


difference_percent=(difference/float(yesterday_Closing_Price)*100)
print(difference_percent)