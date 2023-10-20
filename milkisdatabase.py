"""
MILKIS VENDING MACHINE DATABASE INTERACTION CODE

1. Create the database with four tables: Inventory, Order history, vending machines
"""

from pydantic import BaseModel
from model import Product
import sqlite3
from prettytable import PrettyTable

DB_FILE = 'milkis.db'

conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# Creating the inventory table in the database
cursor.execute('''
    CREATE TABLE IF NOT EXISTS inventory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_name TEXT NOT NULL UNIQUE,
        price REAL NOT NULL,
        product_company TEXT DEFAULT NULL,
        quantity INTEGER DEFAULT 0
    )
''')

# Creating the Order History table in the database
cursor.execute('''
CREATE TABLE IF NOT EXISTS orderhistory (
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER,
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    cost REAL NOT NULL,
    quantity INTEGER NOT NULL,
    FOREIGN KEY (product_id) REFERENCES inventory(id)
)
''')

conn.commit()


###INVENTORY TABLE OPERATIONS###
def create_product(product: Product):
    # Creates a new unique product in the database

    cursor.execute('''
        INSERT INTO inventory (product_name, price, product_company, quantity)
        VALUES (?, ?, ?, ?)
    ''', (product.product_name, product.price, product.product_company, product.quantity))
    conn.commit()


def get_products():
    # Returns a list of all products in the database

    cursor.execute('SELECT id, product_name, price, product_company, quantity FROM inventory')
    products = cursor.fetchall()
    return products


def get_product(product_id: int):
    # Function to return a single product with the product_id identifier

    cursor.execute('SELECT product_name, price FROM inventory WHERE id = ?', (product_id,))
    product = cursor.fetchone()
    return product


def update_product(product_id: int, product: Product):
    # Pass a new product object to update the product at the location of the product id in the database

    cursor.execute('''
        UPDATE inventory
        SET product_name = ?, price = ?
        WHERE id = ?
    ''', (product.product_name, product.price, product_id))
    conn.commit()
    return product


def add_quantity(item_name: str, quantity_to_add: int = 1):
    # modify the item in the database to add some integer quantity
    # wil mainly be used when putting in orders

    cursor.execute("UPDATE inventory SET quantity = quantity + ? WHERE product_name = ?", (quantity_to_add, item_name))
    conn.commit()
    return True


def delete_productID(product_id: int):
    # Delete a product by ID from the database

    cursor.execute('DELETE FROM inventory WHERE id = ?', (product_id,))
    conn.commit()
    return {"message": "Product deleted"}


def delete_productname(product_name: str):
    # Check if the product exists in the database
    cursor.execute('SELECT COUNT(*) FROM inventory WHERE product_name = ?', (product_name,))
    count = cursor.fetchone()[0]

    if count == 0:
        return {"message": "Product not found"}

    # Delete the product from the database
    cursor.execute('DELETE FROM inventory WHERE product_name = ?', (product_name,))
    conn.commit()

    return {"message": "Product deleted"}


def display_inventory_table():
    # Display the entire inventory as a table

    try:
        # Execute a SELECT query to retrieve all entries from the inventory table
        cursor.execute('SELECT * FROM inventory')
        products = cursor.fetchall()

        if not products:
            return {"message": "No products found in the inventory"}

        # Create a PrettyTable to display the inventory
        table = PrettyTable()
        table.field_names = ["ID", "Product Name", "Price", "Product Company", "Quantity"]

        for product in products:
            table.add_row(product)

        return {"message": "Inventory:", "table": table.get_string()}

    except sqlite3.Error as e:
        return {"message": f"Error: {e}"}


def shutdown_event():
    conn.close()


###INVENTORY TABLE OPERTATIONS END###


###TRANSACTION TABLE OPERATIONS###
def order(product_id: int, qty: int):
    # orders a quantity of the product and creates an entry in the order history table

    try:
        # Find the product in the inventory and get its current quantity
        cursor.execute('SELECT product_name, quantity, price FROM inventory WHERE id = ?', (product_id,))
        product_info = cursor.fetchone()

        if product_info is None:
            return {"message": "Product not found"}

        product_name, current_quantity, product_price = product_info

        # Calculate the new quantity after adding qty
        new_quantity = current_quantity + qty
        cost = product_price * qty

        # Update the quantity in the inventory table
        add_quantity(product_name, qty)

        # cursor.execute('UPDATE inventory SET quantity = ? WHERE id = ?', (new_quantity, product_id))
        conn.commit()

        # Insert a new row into the orderhistory table
        cursor.execute('INSERT INTO orderhistory (product_id, cost, quantity) VALUES (?, ?, ?)',
                       (product_id, cost, qty))  # You need to specify the actual price and price_per_product values
        conn.commit()

        return {"message": f"Ordered {qty} {product_name}(s)"}

    except sqlite3.Error as e:
        return {"message": f"Error: {e}"}


def void_order(transaction_id: int):
    # Void an order by the transaction id

    try:
        # Check if the transaction exists in the orderhistory table
        cursor.execute('SELECT * FROM orderhistory WHERE transaction_id = ?', (transaction_id,))
        existing_transaction = cursor.fetchone()

        if existing_transaction is None:
            return {"message": "Transaction not found"}

        # Delete the transaction from the orderhistory table
        cursor.execute('DELETE FROM orderhistory WHERE transaction_id = ?', (transaction_id,))
        conn.commit()

        return {"message": f"Transaction {transaction_id} voided"}

    except sqlite3.Error as e:
        return {"message": f"Error: {e}"}


def display_transaction_table():
    # display the transaction table

    try:
        # Execute a SELECT query to retrieve all entries from the orderhistory table
        cursor.execute('SELECT * FROM orderhistory')
        transactions = cursor.fetchall()

        if not transactions:
            return {"message": "No transactions found"}

        # Create a PrettyTable to display the transactions
        table = PrettyTable()
        table.field_names = ["Transaction ID", "Product ID", "Transaction Date", "Price", "Quantity"]

        for transaction in transactions:
            table.add_row(transaction)

        return {"message": "Transactions:", "table": table.get_string()}

    except sqlite3.Error as e:
        return {"message": f"Error: {e}"}


###END OF TRANSACION OPERATIONS###

###TESTING

product = Product.create_basic(product_name="candy", price=0.99)
product2 = Product.create_basic(product_name="chips", price=1.99)

print(get_products())

order(3, 30)

# Example usage:
inventory = display_inventory_table()
if "table" in inventory:
    print(inventory["message"])
    print(inventory["table"])
else:
    print(inventory["message"])

result = display_transaction_table()
if "table" in result:
    print(result["message"])
    print(result["table"])
else:
    print(result["message"])

shutdown_event()