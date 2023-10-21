import unittest
from model import Product
import sqlite3
from prettytable import PrettyTable
from temp import (
    create_product,
    get_products,
    get_product,
    update_product,
    add_quantity,
    delete_productID,
    delete_productname,
    display_inventory_table,
)

class TestDatabase(unittest.TestCase):
    def setUp(self):
        print("\nSetting up...")
        self.db_file = 'temp_file.db'
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()

        # Create Inventory Table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_name TEXT NOT NULL UNIQUE,
                price REAL NOT NULL,
                product_company TEXT DEFAULT NULL,
                quantity INTEGER DEFAULT 0
            )
        ''')

        #Create OrderHistory Table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS orderhistory (
                transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER,
                transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                cost REAL NOT NULL,
                quantity INTEGER NOT NULL,
                FOREIGN KEY (product_id) REFERENCES inventory(id)
            )
        ''')

        self.conn.commit()

    def tearDown(self):
        print("\nTearing down...")
        self.cursor.execute('DELETE FROM inventory')
        self.cursor.execute('DELETE FROM orderhistory')
        self.conn.commit()
        self.conn.close()

    
    def test_create_product(self):
        print("\nIn Test_create_product...")
        product = Product(product_name="Apple Juice", price=3.99, product_company="Treetop", quantity=20)
        create_product(product, self.conn)
        products = get_products(self.conn)
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0][1], "Apple Juice")
        self.assertEqual(products[0][2], 3.99)
        self.assertEqual(products[0][3], "Treetop")
        self.assertEqual(products[0][4], 20)
    
    
    def test_get_products(self):
        print("\nIn test_get_products...")
        product1 = Product(product_name="Sprite", price=3.99, quantity=24)
        product2 = Product(product_name="7 UP", price=3.99, quantity=24)
        create_product(product1, self.conn)
        create_product(product2, self.conn)
        products = get_products(self.conn)
        self.assertEqual(len(products), 2)
        self.assertEqual(products[0][1], "Sprite")
        self.assertEqual(products[1][1], "7 UP")
    
    def test_get_product(self):
        print("\nIn test_get_product")
        product = Product(product_name="Popcorn", price=1.99, quantity=60)
        create_product(product, self.conn)
        product_id = get_products(self.conn)[0][0]
        retrieved_product = get_product(self.conn, product_id)
        self.assertEqual(retrieved_product[0], "Popcorn")
        self.assertEqual(retrieved_product[1], 1.99)
    
        
    def test_update_product(self):
        # Insert a product into the inventory for testing
        print("\nIn test_update_product")
        self.cursor.execute("INSERT INTO inventory (product_name, price) VALUES (?, ?)", ('Iced Coffee', 5.99))
        inserted_id = self.cursor.lastrowid
        self.conn.commit()

        
        # Update the product
        updated_product = Product(product_name='Iced Coffee', price=7.99)
        updated_product_id = inserted_id  
        result = update_product(self.conn, updated_product_id, updated_product)

        # Fetch the updated product from the database
        self.cursor.execute("SELECT product_name, price FROM inventory WHERE id = ?", (updated_product_id,))
        fetched_product = self.cursor.fetchone()

        self.assertEqual(result, updated_product)  # Check the return value
        
        self.assertEqual(fetched_product, ('Iced Coffee', 7.99))  # Check the database entry

    def test_add_quantity(self):
        print("\nIn test_add_quantity...")
        
        # Create a product in the inventory with an initial quantity of 19
        product = Product(product_name="Pepsi", price=3.99, quantity=19)
        create_product(product, self.conn)
        
        # Add 5 more units of the same product
        item_name = "Pepsi"
        quantity_to_add = 5
        add_quantity(self.conn, item_name, quantity_to_add)
        
        # Retrieve the updated quantity from the database
        self.cursor.execute("SELECT quantity FROM inventory WHERE product_name = ?", (item_name,))
        updated_quantity = self.cursor.fetchone()[0]
        
        self.assertEqual(updated_quantity, 19 + quantity_to_add)  # Check if quantity was updated correctly

    def test_delete_productID(self):
        print("\nIn test_delete_productID...")
        
        # Create a product in the inventory
        product = Product(product_name="Pretzels", price=2.99, quantity=5)
        create_product(product, self.conn)
        
        # Retrieve the product's ID
        self.cursor.execute("SELECT id FROM inventory WHERE product_name = ?", ("Pretzels",))
        product_id = self.cursor.fetchone()[0]
        
        # Delete the product using the delete_productID method
        result = delete_productID(product_id, self.conn)
        
        # Verify that the product has been deleted from the database
        self.cursor.execute("SELECT * FROM inventory WHERE id = ?", (product_id,))
        deleted_product = self.cursor.fetchone()
        
        self.assertIsNone(deleted_product)  # Check if the product has been deleted
        self.assertEqual(result, {"message": "Product deleted"})  # Check the return value

    def test_delete_productname(self):
        print("\nIn test_delete_productname...")

        # Create a product in the inventory
        product = Product(product_name="Lemonade", price=3.99, quantity=5)
        create_product(product, self.conn)

        # Delete the product using the delete_productname method
        product_name = "Lemonade"
        result = delete_productname(product_name, self.conn)

        # Verify that the product has been deleted from the database
        self.cursor.execute("SELECT * FROM inventory WHERE product_name = ?", (product_name,))
        deleted_product = self.cursor.fetchone()

        self.assertIsNone(deleted_product)  # Check if the product has been deleted
        self.assertEqual(result, {"message": "Product deleted"})  # Check the return value

    def test_delete_productname_not_found(self):
        print("\nIn test_delete_productname_not_found...")

        # Attempt to delete a product that doesn't exist
        product_name = "Ultraboost"
        result = delete_productname(product_name, self.conn)

        # Verify that the product was not found and not deleted
        self.assertEqual(result, {"message": "Product not found"})  #Check the return value


    def test_display_inventory_table(self):
        print("\nIn test_display_inventory_table...\n")

        # Create a few products in the inventory
        product1 = Product(product_name="Hersey Bar", price=2.99, quantity=30)
        product2 = Product(product_name="Gatorade", price=3.99, quantity=20)
        create_product(product1, self.conn)
        create_product(product2, self.conn)

        # Call the display_inventory_table method
        result = display_inventory_table(self.conn)

        # Print the message
        print(result["message"])

        # Print the table
        print(result["table"])

        # Verify that the result contains the expected table
        self.assertTrue("Inventory:" in result["message"])
        self.assertTrue("Hersey Bar" in result["table"])
        self.assertTrue("Gatorade" in result["table"])


if __name__ == '__main__':
    unittest.main()
