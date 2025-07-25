import json
import logging
import os
from datetime import datetime

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("utils")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("logs/utils.log", "a", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(filename)s %(funcName)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_cards_data(end_date: str):
    """Функция, которая возвращает общие суммы расходов и кешбэк по каждой карте"""
    df = pd.read_excel("data/operations.xlsx")
    logger.info("DataFrame загружен из файла")
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], format="%d.%m.%Y %H:%M:%S", dayfirst=True,
                                         errors="coerce")
    end_date = pd.to_datetime(end_date, format="%d.%m.%Y %H:%M:%S", dayfirst=True, errors="coerce")
    start_date = end_date.replace(day=1)
    df = df[(df["Дата операции"] >= start_date) & (df["Дата операции"] <= end_date)]
    logger.info("Определение диапазона дат")
    df = df[df["Статус"] == "OK"]
    df = df[df["Сумма платежа"] < 0]
    logger.info("Фильтрация по статусу и сумме платежа")
    card_spending = df.groupby("Номер карты")["Сумма платежа"].sum().abs()
    card_s = []
    logger.info("Создание списка результатов")
    for card, total_spent in card_spending.items():
        last_digits = card.replace("*", "")[-4:]
        cashback = round(total_spent * 0.01, 2)
        card_s.append({
            "last_digits": last_digits,
            "total_spent": round(total_spent, 2),
            "cashback": cashback
        })
    return card_s


def get_top_transactions(end_date: str):
    """Функция, которая возвращает топ-5 транзакций по сумме платежа"""
    df = pd.read_excel("data/operations.xlsx")
    logger.info("DataFrame загружен из файла")
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], format="%d.%m.%Y %H:%M:%S", dayfirst=True,
                                         errors="coerce")
    end_date = pd.to_datetime(end_date, format="%d.%m.%Y %H:%M:%S", dayfirst=True, errors="coerce")
    start_date = end_date.replace(day=1)
    df = df[(df["Дата операции"] >= start_date) & (df["Дата операции"] <= end_date)]
    logger.info("Определение диапазона дат")
    df = df[df["Статус"] == "OK"]
    logger.info("Фильтрация по статусу")
    top_transactions = df.iloc[df['Сумма платежа'].abs().argsort()[::-1]].head(5)
    logger.info("Сортировка по сумме платежа")
    transactions_t = []
    logger.info("Создание списка результатов")
    for _, row in top_transactions.iterrows():
        transaction = {
            "date": row["Дата платежа"],
            "amount": float(row['Сумма платежа']),
            "category": str(row['Категория']) if pd.notna(row['Категория']) else "N/A",
            "description": str(row['Описание']) if pd.notna(row['Описание']) else "N/A"
        }
        transactions_t.append(transaction)
    return transactions_t


def get_greeting():
    """Функция, которая возвращает приветствие в зависимости от времени суток"""
    now = datetime.now().hour
    if 5 <= now < 12:
        return "Доброе утро"
    elif 12 <= now < 17:
        return "Добрый день"
    elif 17 <= now < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def get_settings(filename: str = "user_settings.json") -> dict:
    """Функция, которая возвращает данные из JSON-файла"""
    with open(filename, "r") as file:
        logger.info("Преобразование JSON-файла с кодами валют и акций")
        settings = json.load(file)
        return settings


def get_rates():
    """Функция, которая возвращает курсы валют по запросу"""
    i = 0
    rates_data = []
    while i < 2:
        n = get_settings()["user_currencies"][i]
        url = f"https://api.apilayer.com/exchangerates_data/latest?symbols={"RUB"}&base={n}"
        headers = {"apikey": os.getenv("APILAYER_KEY")}
        response = requests.get(url, headers=headers)
        logger.info("Отправка API-запроса на получение курсов валют")
        i += 1
        data_r = {"currency": n, "rate": round(response.json()["rates"]["RUB"], 2)}
        logger.info("Создание списка результатов с курсами валют")
        rates_data.append(data_r)
    return rates_data


def get_stocks():
    """Функция, которая возвращает стоимость акций по запросу"""
    i = 0
    stocs_data = []
    while i < 5:
        n = get_settings()["user_stocks"][i]
        params = {"symbol": n, "apikey": "iksNrp7CHwKlm98ZCnCcdAbvWmy9OBl6", "from": "2025-07-16"}
        result = requests.get("https://financialmodelingprep.com/stable/historical-price-eod/light", params=params)
        logger.info("Отправка API-запроса на получение стомости акций")
        i += 1
        data_s = {'stock': n, "price": result.json()[0]["price"]}
        logger.info("Создание списка результатов с стоимостями акций")
        stocs_data.append(data_s)
    return stocs_data


# print(get_settings()["user_currencies"][0])
# print(get_rates())
# print(get_stocks())
# print(get_greeting())
# get_cards_data("05.12.2021 00:00:00")
# get_top_transactions("05.12.2021 00:00:00")
# get_rates()
# get_stocks()
