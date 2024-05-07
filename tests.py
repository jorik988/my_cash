import unittest
from app import MyCash


class TestMyCash(unittest.TestCase):
    def setUp(self):
        self.username = 'test_user'
        self.app = MyCash(self.username)
        self.app.records = []

    def test_add_record(self):
        initial_length = len(self.app.records)
        self.app.add_record('2024-05-02', 'Доход', 30000, 'Зарплата')
        self.assertEqual(len(self.app.records), initial_length + 1)

    def test_edit_record(self):
        self.app.add_record('2024-05-02', 'Доход', 30000, 'Зарплата')
        record_id = len(self.app.records) - 1
        self.app.edit_record(record_id, '2024-05-03', 'Расход', 1500, 'Покупка продуктов')
        record = self.app.records[record_id]
        self.assertEqual(record.date, '2024-05-03')
        self.assertEqual(record.category, 'Расход')
        self.assertEqual(record.price, 1500)
        self.assertEqual(record.description, 'Покупка продуктов')

    def test_search_records(self):
        self.app.add_record('2024-05-02', 'Доход', 30000, 'Зарплата')
        self.app.add_record('2024-05-03', 'Расход', 1500, 'Покупка продуктов')
        results = self.app.search_records(category='Расход')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].category, 'Расход')

    def test_display_balance(self):
        self.app.add_record('2024-05-02', 'Доход', 30000, 'Зарплата')
        self.app.add_record('2024-05-03', 'Расход', 1500, 'Покупка продуктов')
        balance, income, expense = self.app.display_balance()
        self.assertEqual(balance, 30000 - 1500)
        self.assertEqual(income, 30000)
        self.assertEqual(expense, 1500)

if __name__ == "__main__":
    unittest.main()