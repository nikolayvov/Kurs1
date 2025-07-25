from reports import spending_by_category
from services import transactions_search
from views import main_page


def main():
    print("Главная страница")
    user_data_1 = input("Введите дату и время для сумирования расходов внутри месяца до заданой даты \n"
                        "и топ-5 транзакций ")
    print(main_page(user_data_1))
    user_data_2 = input("Введите строку для фильтрации расходов ")
    print(transactions_search(user_data_2))
    user_data_3 = input("Введите категорию для фильтрации расходов ")
    user_data_4 = input("Введите дату и время для фильтрации расходов по категории за 3 месяца от заданой даты ")
    print(spending_by_category(user_data_3, user_data_4))
    print("Вывод данных завершен")


main()
