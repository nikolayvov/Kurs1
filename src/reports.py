import logging
from typing import Callable, Optional

import pandas as pd

logger = logging.getLogger("reports")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("logs/reports.log", "a", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(filename)s %(funcName)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def report_to_file(filename: str = "report.xlsx") -> Callable:
    """
        Декоратор, который записывает вывод функции в excel-файл """
    def decorator(func):
        def wrapper(*args, **kwargs):
            result: pd.DataFrame = func(*args, **kwargs)
            result.to_excel(filename)
            logger.info("Запись возврата функции в excel-файл")
            return result
        return wrapper
    return decorator


@report_to_file()
def spending_by_category(category: str, end_date: Optional[str] = None) -> pd.DataFrame:
    """
    Функция, которая возвращает траты за последние 3 месяца по заданой категории от заданой даты. """
    df = pd.read_excel("data/operations.xlsx")
    logger.info("DataFrame загружен из файла")
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], format="%d.%m.%Y %H:%M:%S", dayfirst=True,
                                         errors="coerce")
    logger.info("Определение диапазона дат")
    if end_date is None:
        end_date_dt = pd.Timestamp.now()
    else:
        end_date_dt = pd.to_datetime(end_date, format="%d.%m.%Y %H:%M:%S", dayfirst=True, errors="coerce")
    start_date = end_date_dt - pd.DateOffset(months=3)
    df = df[(df["Дата операции"] >= start_date) & (df["Дата операции"] <= end_date_dt)]
    df = df[df["Статус"] == "OK"]
    df = df[df["Категория"] == category]
    df = df[df["Сумма операции"] < 0]
    logger.info("Фильтрации и возврат результата")
    return df


spending_by_category("Цветы", "31.12.2021 00:00:00")
