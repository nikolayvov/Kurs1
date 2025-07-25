from unittest.mock import patch

import numpy as np
import pandas as pd

from src.reports import spending_by_category


@patch("pandas.read_excel")
def test_spending_by_category(mock_read_excel, transactions_df):
    mock_read_excel.return_value = transactions_df
    result = spending_by_category("Различные товары", "31.12.2021 23:59:59")
    expected_data = [
        {'Дата операции':  pd.to_datetime('31.12.2021 01:23:42',  errors='coerce', dayfirst=True),
         'Дата платежа': pd.to_datetime('31.12.2021', errors='coerce', dayfirst=True), 'Номер карты': '*5091',
         'Статус': 'OK', 'Сумма операции': -564.0, 'Валюта операции': 'RUB', 'Сумма платежа': -564.0,
         'Валюта платежа': 'RUB', 'Кэшбэк': np.nan, 'Категория': 'Различные товары', 'MCC': 5399.0,
         'Описание': 'Ozon.ru', 'Бонусы (включая кэшбэк)': 5, 'Округление на инвесткопилку': 0,
         'Сумма операции с округлением': 564.0}
    ]
    expected = pd.DataFrame(expected_data)
    expected = expected[result.columns]
    expected['Дата платежа'] = expected['Дата платежа'].dt.strftime('%d.%m.%Y')
    result['Дата платежа'] = pd.to_datetime(result['Дата платежа'], dayfirst=True, errors='coerce').dt.strftime(
        '%d.%m.%Y')
    pd.testing.assert_frame_equal(result.reset_index(drop=True), expected.reset_index(drop=True))
