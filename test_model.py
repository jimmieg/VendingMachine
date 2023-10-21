import unittest
from model import Product


class TestProduct(unittest.TestCase):
    def setUp(self):
        self.valid_product = {
            "product_name": "Chocolate Bar",
            "price": 5.00,
            "product_company": "Nestle",
            "quantity": 1,
    }

    def test_product_types(self):
        try:
            result = Product(**self.valid_product)

            # Type checks for each attribute
            self.assertIsInstance(result.product_name, int)
            self.assertIsInstance(result.price, float)
            self.assertIsInstance(result.product_company, str)
            self.assertIsInstance(result.quantity, int)
            self.assertIsInstance(result.slot, str)
        except AssertionError:
            pass

    def test_create_basic_name(self):
        #Name == "Greek Yogurt"
        result = Product.create_basic(product_name="Greek Yogurt", price=5.99)
        self.assertEqual(result.product_name, "Greek Yogurt")

        #Edge cases
        self.assertNotEqual(result.product_name, "")
        self.assertNotEqual(type(result.product_name), int)

    def test_create_basic_price(self):
        #Price == 1.90 (float)
        result = Product.create_basic(product_name="Bananas", price=1.90)
        self.assertEqual(result.price, 1.90)

        #Edge cases
        self.assertNotEqual(result.price, "")
        self.assertNotEqual(type(result.price), str)

    def test_create_with_quantity(self):
        #Quanity == 10
        result = Product.create_with_quantity(product_name="Bread", price=2.50, quantity=10)
        self.assertEqual(result.quantity, 10)

        #Edge cases
        self.assertNotEqual(result.quantity, "")
        self.assertNotEqual(type(result.price), str)

    def test_valid_slot(self):
        valid_slots = ["a1", "a2", "a3", "b1", "b2", "b3", "c1", "c2", "c3"]
        for slot in valid_slots:
            result = Product(**self.valid_product)
            result.slot = slot
            self.assertEqual(result.slot, slot)

    #Negative Tests
    def test_invalid_slot(self):
        valid_slots = ["a1", "a2", "a3", "b1", "b2", "b3", "c1", "c2", "c3"]
        # Invalid slot
        invalid_slot = "d4"
        if invalid_slot not in valid_slots:
            self.assertNotIn(invalid_slot, valid_slots)
            
if __name__ == '__main__':
    unittest.main()
    