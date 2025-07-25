import json
import logging

from utils import get_cards_data, get_greeting, get_rates, get_stocks, get_top_transactions

logger = logging.getLogger("views")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("logs/views.log", "a", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(filename)s %(funcName)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def main_page(end_date: str) -> str:
    """Функция, которая связывает функциональности возвращает JSON-ответ по ТЗ"""
    greeting = get_greeting()
    cards_data = get_cards_data(end_date)
    top_transactions = get_top_transactions(end_date)
    rates = get_rates()
    stock_data = get_stocks()
    logger.info("Сбор возвратов вспомогательных функций")
    result = {
        "greeting": greeting,
        "cards": cards_data,
        "top_transactions": top_transactions,
        "currency_rates": rates,
        "stock_prices": stock_data

    }
    logger.info("Создание списка результатов")
    return json.dumps(result, ensure_ascii=False, indent=4)


# print(main_page("05.12.2021 00:00:00"))
main_page("05.12.2021 00:00:00")
