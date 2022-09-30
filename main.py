import pprint
import requests
from apikey import KEY, currency_list
from requests import request, Session
import streamlit as st
import random


class CurrencyExchange:
    def __init__(self):
        amount_currency = 1
        euorpe_currency = "EUR"
        usd_conversion = "USD"
        # Api call
        self.url = f"https://api.apilayer.com/exchangerates_data/convert?to={usd_conversion}&from={euorpe_currency}&amount={amount_currency}"
        s = Session()

        header = {
            "apikey": KEY
        }

        s.headers.update(header)
        self.response = s.get(self.url).json()

        # Making it easier to read code by using pprint

        pprint.pprint(self.response)

        # declaring variables for easier use

        date = self.response["date"]
        rate = self.response["info"]["rate"]
        money_amount = self.response["query"]["amount"]
        converted_from = self.response["query"]["from"]
        converted_to = self.response["query"]["to"]
        result = self.response["result"]

        # streamlit setup
        st.title("Currency Exchange Calculator")

        self.convertOptions = st.selectbox("From", currency_list)
        self.convertToOptions = st.selectbox("To", currency_list)
        self.moneyAmount = st.number_input("$ Amount")
        topCurrencies()

    def GetCurrencyOption(self):
        try:
            st.write(f"### Currency Searched for: ")
            url = f"https://api.apilayer.com/exchangerates_data/convert?to={self.convertToOptions}&from={self.convertOptions}&amount={self.moneyAmount}"
            header = {
                "apikey": KEY
            }
            req = requests.get(url, headers=header)
            res = req.json()
            rate = res["info"]["rate"]
            money_amount = res["query"]["amount"]
            converted_from = res["query"]["from"]
            converted_to = res["query"]["to"]
            result = res["result"]
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Amount", f"${money_amount}", "")
            col2.metric("From", f"{converted_from}", "")
            col3.metric("Converted To", f"{converted_to}", "")
            col4.metric("Result", f"${result}", f"{rate}")
        except KeyError:
            st.error("INFO ERROR - Please change the values")

def topCurrencies():
    st.write("### Top 5 Currencies")
    topArr = ["EUR","GBP","JPY","CAD","AUD"]
    for data in topArr:
        header = {
            "apikey": KEY
        }
        req = requests.get(f"https://api.apilayer.com/exchangerates_data/convert?to=USD&from={data}&amount=1", headers=header)
        res = req.json()
        pprint.pprint(res)

        for x in range(1):
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Amount", f"${res['query']['amount']}", "")
            col2.metric("From", f"{res['query']['from']}", "")
            col3.metric("Converted To", f"{res['query']['to']}", "")
            col4.metric("Result", f"${res['result']}", f"{res['info']['rate']}")



CurrencyExchange().GetCurrencyOption()
