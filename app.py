import json
from datetime import datetime
import os


class Record:
    """
    Класс для создания объекта финансовой записи.
    """

    def __init__(self, date: str, category: str, price: int, description: str):
        """
        Инициализация новой записи.

        :param date: Дата записи в формате ГГГГ-ММ-ДД.
        :param category: Категория записи ("Доход" или "Расход").
        :param price: Сумма записи.
        :param description: Описание записи.
        """
        self.date = date
        self.category = category
        self.price = price
        self.description = description


class MyCash:
    """
    Класс для управления финансовыми записями пользователя.
    """

    def __init__(self, username: str):
        """
        Инициализация приложения для указанного пользователя.

        :param username: Имя пользователя.
        """
        self.filepath = f"{username}.json"
        self.records: list[Record] = []
        self.load_data()

    def load_data(self):
        """
        Загрузка данных из файла JSON.
        Если файл не найден, инициализируется пустой список записей.
        """
        try:
            with open(self.filepath, "r", encoding="utf-8") as file:
                data = json.load(file)
                for record in data:
                    self.records.append(Record(**record))
        except FileNotFoundError:
            self.records = []

    def save_data(self):
        """
        Сохранение текущих данных в файл JSON.
        """
        data = [record.__dict__ for record in self.records]
        with open(self.filepath, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def add_record(self, date: str, category: str, price: int, description: str):
        """
        Добавление новой записи и сохранение данных.

        :param date: Дата новой записи в формате ГГГГ-ММ-ДД.
        :param category: Категория новой записи ("Доход" или "Расход").
        :param price: Сумма новой записи.
        :param description: Описание новой записи.
        """
        self.records.append(Record(date, category, price, description))
        self.save_data()

    def edit_record(
        self,
        record_id: int,
        date: str = None,
        category: str = None,
        price: int = None,
        description: str = None,
    ):
        """
        Редактирование существующей записи и сохранение данных.

        :param record_id: ID записи для редактирования.
        :param date: Новая дата записи в формате ГГГГ-ММ-ДД.
        :param category: Новая категория записи ("Доход" или "Расход").
        :param price: Новая сумма записи.
        :param description: Новое описание записи.
        """
        record = self.records[record_id]
        if date:
            record.date = date
        if category:
            record.category = category
        if price:
            record.price = price
        if description:
            record.description = description
        self.save_data()

    def search_records(self, category: str = None, date: str = None, price: int = None):
        """
        Поиск записей по категории, дате и/или сумме.

        :param category: Категория для поиска ("Доход" или "Расход").
        :param date: Дата для поиска в формате ГГГГ-ММ-ДД.
        :param price: Сумма для поиска.
        :return: Список записей, которые соответствуют критериям поиска.
        """
        results = []
        for record in self.records:
            if category and category != record.category:
                continue
            if date:
                record_date_parts = record.date.split("-")
                input_date_parts = date.split("-")
                if record_date_parts[: len(input_date_parts)] != input_date_parts:
                    continue
            if price and price != record.price:
                continue
            results.append(record)
        return results

    def display_balance(self):
        """
        Расчет и вывод баланса, доходов и расходов.

        :return: Кортеж из трех элементов: баланс, доходы и расходы.
        """
        income = sum(
            record.price for record in self.records if record.category == "Доход"
        )
        expense = sum(
            record.price for record in self.records if record.category == "Расход"
        )
        balance = income - expense
        return balance, income, expense

    def run(self):
        """
        Запуск основного цикла приложения, включая пользовательский интерфейс.

        Метод выводит меню действий, принимает ввод от пользователя и 
        вызывает методы для обработки действий.
        """
        while True:
            print("\n1. Показать текущий баланс")
            print("2. Добавление новой записи")
            print("3. Редактирование записи")
            print("4. Поиск записи")
            print("5. Выход\n")
            choice = input("Выберите действие: ")
            print()
            if choice not in ["1", "2", "3", "4", "5"]:
                print("Неверный выбор. Пожалуйста, попробуйте снова.")
                continue
            if choice == "1":
                balance, income, expense = self.display_balance()
                print(f"Баланс: {balance}, Доходы: {income}, Расходы: {expense}")
            elif choice == "2":
                date = datetime.now().strftime("%Y-%m-%d")
                category_choice = input("Выберите категорию (1 - Доход, 2 - Расход): ")
                if category_choice not in ["1", "2"]:
                    print("\nНеверный выбор категории. Пожалуйста, попробуйте снова.")
                    continue
                category = "Доход" if category_choice == "1" else "Расход"
                try:
                    price = int(input("Введите сумму: "))
                    if price < 0:
                        raise ValueError("\nСумма не может быть отрицательной.")
                except ValueError:
                    print("\nНекорректный ввод суммы. Пожалуйста, введите число.")
                    continue
                description = input("Введите описание: ")
                self.add_record(date, category, price, description)
            elif choice == "3":
                try:
                    record_id = int(input("Введите ID записи для редактирования: "))
                    if record_id < 0 or record_id >= len(self.records):
                        print(
                            "Запись с таким ID не существует. Пожалуйста, попробуйте снова."
                        )
                        continue
                except ValueError:
                    print("\nНекорректный ввод ID записи. Пожалуйста, введите число.")
                    continue
                category_choice = input(
                    "Введите новую категорию: 1 - Доход, 2 - Расход (оставьте пустым, чтобы не менять): "
                )
                if category_choice not in ["1", "2", ""]:
                    print("\nНеверный выбор категории. Пожалуйста, попробуйте снова.")
                    continue
                category = (
                    "Доход"
                    if category_choice == "1"
                    else "Расход" if category_choice == "2" else None
                )
                date = input(
                    "Введите новую дату в формате ГГГГ-ММ-ДД (оставьте пустым, чтобы не менять): "
                )
                if date:
                    try:
                        datetime.strptime(date, "%Y-%m-%d")
                    except ValueError:
                        print(
                            "\nНекорректный формат даты. Пожалуйста, введите дату в формате ГГГГ-ММ-ДД."
                        )
                        continue

                price = input(
                    "Введите новую сумму (оставьте пустым, чтобы не менять): "
                )
                if price:
                    try:
                        price = int(price)
                        if price < 0:
                            print("\nСумма не может быть отрицательной.")
                            continue
                    except ValueError:
                        print(
                            "\nНекорректный ввод суммы. Пожалуйста, введите положительное число."
                        )
                        continue

                description = input(
                    "Введите новое описание (оставьте пустым, чтобы не менять): "
                )
                self.edit_record(
                    record_id,
                    date if date else None,
                    category,
                    int(price) if price else None,
                    description,
                )
            elif choice == "4":
                category_choice = input(
                    "Введите категорию для поиска: 1 - Доход, 2 - Расход (Оставьте пустым, чтобы искать по всем категориям): "
                )
                category = (
                    "Доход"
                    if category_choice == "1"
                    else "Расход" if category_choice == "2" else None
                )
                date = input(
                    "Введите дату для поиска в формате ГГГГ-ММ-ДД, ГГГГ-ММ или ГГГГ (Оставьте пустым, чтобы искать по всем датам): "
                )
                if date:
                    try:
                        if len(date) == 4:  # ГГГГ
                            datetime.strptime(date, "%Y")
                        elif len(date) == 7:  # ГГГГ-ММ
                            datetime.strptime(date, "%Y-%m")
                        elif len(date) == 10:  # ГГГГ-ММ-ДД
                            datetime.strptime(date, "%Y-%m-%d")
                        else:
                            raise ValueError
                    except ValueError:
                        print(
                            "\nНекорректный формат даты. Пожалуйста, введите дату в формате ГГГГ-ММ-ДД, ГГГГ-ММ или ГГГГ."
                        )
                        continue
                price = input(
                    "Введите сумму для поиска (оставьте пустым, чтобы искать по всем суммам): "
                )
                if price:
                    try:
                        price = int(price)
                        if price < 0:
                            print(
                                "\nСумма не может быть отрицательной, попробуйте заново."
                            )
                            continue
                    except ValueError:
                        print("\nНекорректный ввод суммы. Пожалуйста, введите число.")
                        continue

                results = self.search_records(
                    category, date if date else None, int(price) if price else None
                )
                if not results:
                    print("\nПо вашему запросу записей не найдено.")
                else:
                    for record in results:
                        print(
                            f"ID: {self.records.index(record)}, Дата: {record.date}, Категория: {record.category}, Сумма: {record.price}, Описание: {record.description}"
                        )
            elif choice == "5":
                break
            else:
                print("Неверный выбор. Пожалуйста, попробуйте снова.")


def get_username() -> str:
    """
    Получение имени пользователя.

    Метод запрашивает ввод имени пользователя и проверяет, существует ли файл с данными для этого пользователя.
    Если файл не существует, метод предлагает пользователю создать нового пользователя или ввести имя пользователя заново.
    """
    while True:
        username = input("Введите имя пользователя: ")
        if os.path.exists(f"{username}.json"):
            return username
        else:
            print(f'Пользователь с именем "{username}" не найден.')
            choice = input(
                "Создать нового пользователя? 1 - Создать пользователя, 2 - Ввести заново: "
            )
            if choice == "1":
                return username


if __name__ == "__main__":
    username: str = get_username()
    app: MyCash = MyCash(username)
    app.run()
    # Этот блок кода  запрашивает имя пользователя
    # создает новый экземпляр приложения для этого пользователя 
    # и запускает основной цикл приложения.
    
