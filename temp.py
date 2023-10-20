import unittest
import sqlite3
from model import Product
from inventorytesting import create_product, get_product

TEST_DB_FILE = 'test.db'


class TestInventoryTesting(unittest.TestCase):
    def setUp(self):
        print("\nSetting Up....")
        self.conn = sqlite3.connect(TEST_DB_FILE)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
			CREATE TABLE IF NOT EXISTS products (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				product_name TEXT NOT NULL,
				price REAL NOT NULL,
				product_company TEXT DEFAULT NULL,
				quantity INTEGER DEFAULT 0,
				slot TEXT UNIQUE CHECK (slot IN ('a1', 'a2', 'a3', 'b1', 'b2', 'b3', 'c1', 'c2', 'c3')) DEFAULT NULL
			)
		''')
        self.conn.commit()

    def test_create_product(self):
        print("Testing create_product")
        product = Product(product_name="test_product", price=1.0, product_company="test_company", quantity=10)
        print(product)
        create_product(product)
        result = get_product(1)  # Assume Key == 1
        self.assertEqual(result, ("test_product", 1.0))

    def tearDown(self):
        print("Tearing Down")
        self.conn.close()


if __name__ == '__main__':
    unittest.main()
