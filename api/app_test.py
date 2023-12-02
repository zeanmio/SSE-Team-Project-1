import unittest
from app import app


class AppTestCase(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_form_page_loads(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"City Explorer", response.data)

    def test_city_info_page(self):
        response = self.app.get(
            "/get-city-info?city=London&username=test&country=UK&date=2023-12-31"
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Tourist Attractions", response.data)
        self.assertIn(b"Upcoming Events", response.data)
        self.assertIn(b"Weather", response.data)


if __name__ == "__main__":
    unittest.main()
