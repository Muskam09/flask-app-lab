import unittest
from app import app


class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        """Налаштування клієнта тестування перед кожним тестом."""
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_products_page(self):
        """Тест маршруту /products."""
        response = self.client.get("/products/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Iphone", response.data)
        self.assertIn(b"Ipad", response.data)
        self.assertIn(b"MacBook", response.data)
        self.assertIn(b"Apple Watch", response.data)

    def test_detail_product_page(self):
        """Тест маршруту /products/<id>."""
        response = self.client.get("/products/1")
        self.assertIn(b'1', response.data)
        self.assertIn(b"Iphone", response.data)
        self.assertIn(
            b"A line of smartphones",
            response.data
        )


if __name__ == "__main__":
    unittest.main()