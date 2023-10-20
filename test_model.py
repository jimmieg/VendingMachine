import unittest
from model import Product


class TestProduct(unittest.TestCase):
    def test_create_basic_name(self):
        result = Product.create_basic(product_name="Greek Yogurt", price=5.99)
        self.assertEqual(result.product_name, "Greek Yogurt")

    def test_create_basic_price(self):
        result = Product.create_basic(product_name="Bananas", price=1.90)
        self.assertEqual(result.price, 1.90)

    def test_create_with_quantity(self):
        result = Product.create_with_quantity(product_name="Bread", price=2.50, quantity=10)
        self.assertEqual(result.quantity, 10)


if __name__ == '__main__':
    unittest.main()
