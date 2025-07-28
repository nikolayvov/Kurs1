from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest

from src.utils import get_cards_data, get_greeting, get_rates, get_top_transactions


@patch("pandas.read_excel")
def test_get_cards_data(mock_read_excel, transactions_df):
    mock_read_excel.return_value = transactions_df
    result = get_cards_data("31.12.2021 23:59:59")
    expected = [
                {"last_digits": "7197", "total_spent": 421.06, "cashback": 4.21},
                {"last_digits": "5091", "total_spent": 571.07, "cashback": 5.71}
    ]
    assert sorted(result, key=lambda x: x["last_digits"]) == sorted(expected, key=lambda x: x["last_digits"])


@patch("pandas.read_excel")
def test_get_top_transactions(mock_read_excel, transactions_df):
    mock_read_excel.return_value = transactions_df
    result = get_top_transactions("31.12.2021 23:59:59")
    expected = [
        {
            "date": "31.12.2021",
            "amount": -20000.0,
            "category": "Переводы",
            "description": "Константин Л."
        },
        {
            "date": "31.12.2021",
            "amount": -800.0,
            "category": "Переводы",
            "description": "Константин Л."
        },
        {
            "date": "31.12.2021",
            "amount": -564.0,
            "category": "Различные товары",
            "description": "Ozon.ru"
        },
        {
            "date": "31.12.2021",
            "amount": -160.89,
            "category": "Супермаркеты",
            "description": "Колхоз"
        },
        {
            "date": "31.12.2021",
            "amount": -118.12,
            "category": "Супермаркеты",
            "description": "Магнит"
        }
    ]
    assert result == expected


@pytest.mark.parametrize(
    "mock_hour, expected_greeting",
    [
        (6, "Доброе утро"),
        (12, "Добрый день"),
        (17, "Добрый вечер"),
        (4, "Доброй ночи"),
    ]
)
def test_get_greeting(mock_hour, expected_greeting):
    class MockDateTime(datetime):
        @classmethod
        def now(cls):
            return cls(2024, 1, 1, mock_hour, 0, 0)

    with patch("src.utils.datetime", MockDateTime):
        assert get_greeting() == expected_greeting


@patch("requests.get")
@patch("src.utils.get_settings")
def test_get_rates(mock_get_settings, mock_requests_get):
    mock_get_settings.return_value = {"user_currencies": ["USD", "EUR"]}
    mock_resp_usd = MagicMock()
    mock_resp_usd.json.return_value = {"rates": {"RUB": 75.5}}
    mock_resp_eur = MagicMock()
    mock_resp_eur.json.return_value = {"rates": {"RUB": 85.3}}
    mock_requests_get.side_effect = [mock_resp_usd, mock_resp_eur]
    expected = [
        {"currency": "USD", "rate": 75.5},
        {"currency": "EUR", "rate": 85.3}
    ]
    result = get_rates()
    assert result == expected
