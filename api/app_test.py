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
    @patch("app.get_dining_data")
    @patch("app.get_seatgeek_events")
    @patch("app.get_weather_data")
    @patch("app.get_airquality_forecast_data")
    def test_city_info_page(
        self,
        mock_weather_data,
        mock_airquality_forecast_data,
        mock_events_data,
        mock_dining_data,
        mock_places_data,
        mock_db_connection,
    ):
        mock_db_connection.return_value = MagicMock()

        mock_places_data.return_value = ([], 0, 0, None)
        mock_dining_data.return_value =([],0, 0, None)
        mock_events_data.return_value = ([], None)
        mock_weather_data.return_value = (
            {"temperature": {"min": 280, "max": 285}},
            None,
        )
        mock_airquality_forecast_data.return_value = (
            [{"time": 1701864000, "avg_aqi": 2.3333333333333335}, ...],  # Example data
            None,
        )
        response = self.app.get(
            "/get-city-info?city=London&username=test&country=UK&date=2023-12-31"
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Discover", response.data)
        self.assertIn(b"Upcoming Events", response.data)
        self.assertIn(b"Weather", response.data)


if __name__ == "__main__":
    unittest.main()
