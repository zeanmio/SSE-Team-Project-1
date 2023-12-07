import unittest
from unittest.mock import patch, MagicMock
from app import app


class AppTestCase(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_form_page_loads(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"City Explorer", response.data)

    @patch("app.get_db_connection")
    @patch("app.get_places_data")
    @patch("app.get_place_information")
    @patch("app.get_dining_data")
    @patch("app.get_seatgeek_events")
    def test_city_info_page(
        self,
        mock_events_data,
        mock_dining_data,
        mock_place_information,
        mock_places_data,
        mock_db_connection,
    ):
        mock_db_connection.return_value = MagicMock()

        mock_places_data.return_value = ([], 0, 0, None)
        mock_dining_data.return_value = ([], None)
        mock_events_data.return_value = ([], None)
        mock_place_information.return_value = (
            "Example Description",
            ["https://example.com"],
            "example_instagram",
            "example_twitter",
            "example_facebook",
            None,
        )
        response = self.app.get(
            "/get-city-info?city=London&username=test&country=UK&date=2023-12-31"
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Discover", response.data)
        self.assertIn(b"Upcoming Events", response.data)


if __name__ == "__main__":
    unittest.main()
