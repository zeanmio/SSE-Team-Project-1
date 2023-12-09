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

    def test_about_page(self):
        response = self.app.get("/about")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"About", response.data)

    def test_feedback_page(self):
        response = self.app.get("/feedback")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Feedback", response.data)

    def test_submit_feedback_page(self):
        response = self.app.get("/submit-feedback?username=test&feedback=test_feedback")
        self.assertEqual(response.status_code, 302)  # Expecting a redirect

    @patch("app.get_db_connection")
    @patch("app.get_places_data")
    @patch("app.get_place_information")
    def test_places_info_page(
        self,
        mock_place_information,
        mock_places_data,
        mock_db_connection,
    ):
        mock_db_connection.return_value = MagicMock()

        mock_places_data.return_value = ([], 0, 0, None)
        mock_place_information.return_value = (
            "Example Description",
            ["https://example.com"],
            "example_instagram",
            "example_twitter",
            "example_facebook",
            None,
        )
        response = self.app.get(
            "/get-places-info?city=London&username=test&country=UK&date=2023-12-31&attraction_type=architectural&food_type=restaurants"
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Recommended Attractions", response.data)

    @patch("app.get_db_connection")
    @patch("app.get_dining_data")
    @patch("app.get_place_information")
    def test_dining_info_page(
        self,
        mock_place_information,
        mock_dining_data,
        mock_db_connection,
    ):
        mock_db_connection.return_value = MagicMock()

        mock_dining_data.return_value = ([], 0, 0, None)
        mock_place_information.return_value = (
            "Example Description",
            ["https://example.com"],
            "example_instagram",
            "example_twitter",
            "example_facebook",
            None,
        )
        response = self.app.get(
            "/get-dining-info?city=London&username=test&country=UK&date=2023-12-31&attraction_type=architectural&food_type=restaurants"
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Recommended Dining", response.data)

    @patch("app.get_db_connection")
    @patch("app.get_seatgeek_events")
    def test_events_info_page(
        self,
        mock_events_data,
        mock_db_connection,
    ):
        mock_db_connection.return_value = MagicMock()

        mock_events_data.return_value = ([], None)

        response = self.app.get(
            "/get-events-info?city=London&username=test&country=UK&date=2023-12-31&attraction_type=architectural&food_type=restaurants&lat=0&lon=0"
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Upcoming Events", response.data)

    @patch("app.get_db_connection")
    @patch("app.get_places_data")
    @patch("app.get_sunrisesunset_data")
    @patch("app.get_weather_data")
    @patch("app.determine_weather_condition")
    @patch("app.get_airquality_forecast_data")
    def test_weather_info_page(
        self,
        mock_airquality_forecast_data,
        mock_weather_condition,
        mock_weather_data,
        mock_sunrisesunset_data,
        mock_places_data,
        mock_db_connection,
    ):
        mock_db_connection.return_value = MagicMock()

        mock_places_data.return_value = ([], 0, 0, None)

        mock_sunrisesunset_data.return_value = ([], None)

        mock_weather_data.return_value = ([], None)

        mock_weather_condition.return_value = ([], [])

        mock_airquality_forecast_data.return_value = ([], None)

        response = self.app.get(
            "/get-weather-info?city=London&username=test&country=UK&date=2023-12-31&attraction_type=architectural&food_type=restaurants"
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Weather Information", response.data)


if __name__ == "__main__":
    unittest.main()
