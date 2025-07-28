import json
import logging
import re

import pandas as pd

logger = logging.getLogger("services")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("logs/services.log", "a", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(filename)s %(funcName)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def transactions_search(search: str) -> list[dict]:
    """
    Функция возвращает список транзакций, где строка поиска встречается в описании или категории
    """
    data = pd.read_excel("data/operations.xlsx").to_dict(orient="records")
    logger.info("DataFrame загружен из файла")
    result = []
    logger.info("Создание списка результатов")
    re_pattern = re.compile(search, re.IGNORECASE)
    logger.info("Фильтрация по заданной строке")
    for operation in data:
        description = str(operation.get("Описание", ""))
        category = str(operation.get("Категория", ""))
        if re_pattern.search(description) or re_pattern.search(category):
            result.append(operation)
    return json.dumps(result, ensure_ascii=False, indent=2)


# print(transactions_search("Y.M"))
# transactions_search("Y.M")
