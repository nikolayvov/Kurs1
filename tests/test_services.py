import json
import math
from unittest.mock import patch

from src.services import transactions_search


def replace_nan_with_none(data):
    def fix_value(v):
        if isinstance(v, float) and math.isnan(v):
            return None
        return v

    return [{k: fix_value(v) for k, v in item.items()} for item in data]


@patch("pandas.read_excel")
def test_transactions_search(mock_read_excel, transactions_df):
    mock_read_excel.return_value = transactions_df
    result_json = transactions_search("Колхоз")
    result = json.loads(result_json)
    expected = [
        {
            "Дата операции": "31.12.2021 16:44:00",
            "Дата платежа": "31.12.2021",
            "Номер карты": "*7197",
            "Статус": "OK",
            "Сумма операции": -160.89,
            "Валюта операции": "RUB",
            "Сумма платежа": -160.89,
            "Валюта платежа": "RUB",
            "Кэшбэк": None,
            "Категория": "Супермаркеты",
            "MCC": 5411.0,
            "Описание": "Колхоз",
            "Бонусы (включая кэшбэк)": 3,
            "Округление на инвесткопилку": 0,
            "Сумма операции с округлением": 160.89,
        },
        {
            "Дата операции": "31.12.2021 16:42:04",
            "Дата платежа": "31.12.2021",
            "Номер карты": "*7197",
            "Статус": "OK",
            "Сумма операции": -64.0,
            "Валюта операции": "RUB",
            "Сумма платежа": -64.0,
            "Валюта платежа": "RUB",
            "Кэшбэк": None,
            "Категория": "Супермаркеты",
            "MCC": 5411.0,
            "Описание": "Колхоз",
            "Бонусы (включая кэшбэк)": 1,
            "Округление на инвесткопилку": 0,
            "Сумма операции с округлением": 64.0,
        },
        {
            "Дата операции": "31.12.2021 15:44:39",
            "Дата платежа": "31.12.2021",
            "Номер карты": "*7197",
            "Статус": "OK",
            "Сумма операции": -78.05,
            "Валюта операции": "RUB",
            "Сумма платежа": -78.05,
            "Валюта платежа": "RUB",
            "Кэшбэк": None,
            "Категория": "Супермаркеты",
            "MCC": 5411.0,
            "Описание": "Колхоз",
            "Бонусы (включая кэшбэк)": 1,
            "Округление на инвесткопилку": 0,
            "Сумма операции с округлением": 78.05,
        },
    ]
    result_fixed = replace_nan_with_none(result)
    assert result_fixed == expected
