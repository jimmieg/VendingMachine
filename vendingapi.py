from model import Product
import sqlite3

class VendingMachine:
    def __init__(self, db_file = 'vendingmachine.db'):
        self.slots = {}  # A dictionary to represent the vending machine slots (slot_name: product)
        self.db_file = db_file
        self.connection = sqlite3.connect(db_file)
    def load_into(self, slot_name: str, product_identifier: str):
            # Check if a product with the given name or ID exists in the database
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM products WHERE product_name = ? OR product_id = ?", (product_identifier, product_identifier))
            product_data = cursor.fetchone()
            
            if product_data:
                # Product found in the database, create a Product object and load it into the slot
                product = Product(product_id=product_data[0],
                    product_name=product_data[1],
                    price=product_data[2],
                    quantity=product_data[3],
                    product_company=product_data[4]
                )
                self.slots[slot_name] = product
                return True  # Product loaded successfully
            
            return False  # Product not found in the database

    def remove_from(self, slot_name: str):
        """
        Remove a product from a slot in the vending machine.
        
        Args:
            slot_name (str): The name of the slot (e.g., "a1").
        
        Returns:
            Product or None: The removed product, or None if the slot is empty.
        """
        return self.slots.pop(slot_name, None)

    def get_product(self, slot_name: str):
        """
        Get the product information from a slot in the vending machine.
        
        Args:
            slot_name (str): The name of the slot (e.g., "a1").
        
        Returns:
            Product or None: The product in the slot, or None if the slot is empty.
        """
        return self.slots.get(slot_name)

    def list_products(self):
        """
        List all products in the vending machine.
        
        Returns:
            dict: A dictionary representing the vending machine slots and their products.
        """
        return self.slots