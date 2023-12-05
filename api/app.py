from flask import Flask, render_template, request, jsonify, redirect, url_for
from datetime import datetime
import requests, logging, psycopg2, os


app = Flask(__name__)


# SQL
DB_HOST = "db.doc.ic.ac.uk"
DB_USER = "xl6423"
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = "xl6423"
DB_PORT = "5432"


def get_db_connection():
    try:
        connection = psycopg2.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
        )
        return connection
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
        return None


# API
API_KEYS = {
    "opentripmap": os.getenv("OPENTRIPMAP_KEY"),
    "seatgeek_client_id": os.getenv("SEATGEEK_ID"),
    "seatgeek_client_secret": os.getenv("SEATGEEK_SECRET"),
    "openweather": os.getenv("OPENWEATHER_KEY"),
}


BASE_URLS = {
    "opentripmap": "https://api.opentripmap.com",
    "seatgeek": "https://api.seatgeek.com",
    "openweather": "https://api.openweathermap.org",
    "sunrisesunset": "https://api.sunrisesunset.io",
}


# Tourist Attractions
def get_places_data(city):
    geoname_url = f"{BASE_URLS['opentripmap']}/0.1/en/places/geoname?name={city}&apikey={API_KEYS['opentripmap']}"
    geoname_response = requests.get(geoname_url)

    if not geoname_response.ok:
        return None, "Error fetching geoname data from OpenTripMap"

    geoname_data = geoname_response.json()

    if "lon" not in geoname_data or "lat" not in geoname_data:
        return None, "Invalid data received from OpenTripMap"

    lon = geoname_data["lon"]
    lat = geoname_data["lat"]

    places_url = f"{BASE_URLS['opentripmap']}/0.1/en/places/radius?radius=20000&lon={lon}&lat={lat}&rate=3h&limit=100&apikey={API_KEYS['opentripmap']}"
    places_response = requests.get(places_url)

    if not places_response.ok:
        return None, "Error fetching places from OpenTripMap"

    return places_response.json(), lon, lat, None


# Upcoming Events
def get_seatgeek_events(city, date):
    base_url = f"{BASE_URLS['seatgeek']}/2/events"
    params = {
        "client_id": API_KEYS["seatgeek_client_id"],
        "client_secret": API_KEYS["seatgeek_client_secret"],
        "venue.city": city,
        "datetime_local.gte": date,
    }

    response = requests.get(base_url, params=params)

    if response.ok:
        data = response.json()
        events_data = data.get("events", [])
        return events_data, None
    else:
        return None, "Error fetching events from SeatGeek"


# Weather
def get_weather_data(lat, lon, date):
    weather_url = f"{BASE_URLS['openweather']}/data/3.0/onecall/day_summary?lat={lat}&lon={lon}&units=metric&date={date}&appid={API_KEYS['openweather']}"
    response = requests.get(weather_url)
    if not response.ok:
        return None, "Error fetching weather data"
    weather_data = response.json()
    return weather_data, None


def get_sunrisesunset_data(lat, lon, date):
    sunrisesunset_url = (
        f"{BASE_URLS['sunrisesunset']}/json?lat={lat}&lng={lon}&date={date}"
    )
    response = requests.get(sunrisesunset_url)
    if not response.ok:
        return None, "Error fetching sunrisesunset data"

    sunrisesunset_data = response.json()
    return sunrisesunset_data, None


def determine_weather_condition(data):
    cloud_cover = data.get("cloud_cover", {}).get("afternoon", 0)
    humidity = data.get("humidity", {}).get("afternoon", 0)
    precipitation = data.get("precipitation", {}).get("total", 0)
    min_temperature = data.get("temperature", {}).get("min", 0)

    if cloud_cover < 10 and humidity < 40 and precipitation == 0:
        return "Sunny", "01d"
    elif cloud_cover < 30 and precipitation == 0:
        return "Partly cloudy", "02d"
    elif cloud_cover < 70 and precipitation == 0:
        return "Cloudy", "03d"
    elif cloud_cover < 70 and precipitation > 0:
        if precipitation > 5 and min_temperature < 0:
            return "Snowy", "13d"
        else:
            return "Shower Rain", "09d"
    elif cloud_cover >= 70 or precipitation > 0:
        return "Rainy", "10d"


@app.route("/", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        username = request.form.get("username")
        country = request.form.get("country")
        city = request.form.get("city")
        date = request.form.get("date")
        return redirect(url_for("get-city-info", city=city))
    return render_template("index.html")


@app.route("/get-city-info", methods=["GET"])
def get_city_info():
    username = request.args.get("username")
    country = request.args.get("country")
    city = request.args.get("city")
    date = request.args.get("date")

    # Connect to database
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = "INSERT INTO userdata (username, country, city, exploration_date) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (username, country, city, date))
            connection.commit()
            cursor.close()
        except (Exception, psycopg2.Error) as error:
            print("Error while inserting data into Postgres", error)
        finally:
            connection.close()

    # Tourist Attractions
    places_data, lon, lat, places_error = get_places_data(city)
    if places_error:
        logging.error(f"Error in getting places data: {places_error}")
        return jsonify({"error": places_error}), 500

    # Upcoming Events
    events_data, events_error = get_seatgeek_events(city, date)
    if events_error:
        logging.error(f"Error in getting events data: {events_error}")
        return jsonify({"error": events_error}), 500

    # Weather
    min_temp = max_temp = None
    weather_data = {}  # Initialize weather_data as an empty dictionary
    sunrise_time = sunset_time = None  # Initialize sunrise and sunset times

    if places_data and "features" in places_data:
        location = places_data["features"][0]["geometry"]["coordinates"]
        lat, lon = location[1], location[0]

        # Sunrisesunset
        sunrisesunset_data, sunrisesunset_error = get_sunrisesunset_data(lat, lon, date)
        print(sunrisesunset_data)
        if sunrisesunset_error:
            logging.error(f"Error in getting sunrisesunset data: {sunrisesunset_error}")
            return jsonify({"error": sunrisesunset_error}), 500

        # Extract sunrise and sunset times from the API response
        sunrise_str = sunrisesunset_data.get("results", {}).get("sunrise", "")
        sunset_str = sunrisesunset_data.get("results", {}).get("sunset", "")
        golden_hour_str = sunrisesunset_data.get("results", {}).get("golden_hour", "")

        # Parse and format sunrise time, sunset time, and golden hour
        if sunrise_str:
            sunrise_datetime = datetime.strptime(sunrise_str, "%I:%M:%S %p")
            sunrise_time = sunrise_datetime.strftime("%I:%M %p")

        if sunset_str:
            sunset_datetime = datetime.strptime(sunset_str, "%I:%M:%S %p")
            sunset_time = sunset_datetime.strftime("%I:%M %p")
        
        if golden_hour_str:
            golden_hour_datetime = datetime.strptime(golden_hour_str, "%I:%M:%S %p")
            golden_hour_time = golden_hour_datetime.strftime("%I:%M %p")

        print(golden_hour_time)
        # Extract weatehr data from the API response
        weather_data, weather_error = get_weather_data(lat, lon, date)
        if weather_error:
            logging.error(f"Error in getting weather data: {weather_error}")
            return jsonify({"error": weather_error}), 500

        min_temp = round(weather_data["temperature"]["min"])
        max_temp = round(weather_data["temperature"]["max"])
        weather_data["min_temp"] = min_temp
        weather_data["max_temp"] = max_temp

        # Determine weather conditions
        weather_condition, weather_icon = determine_weather_condition(weather_data)
        weather_data["weather_condition"] = weather_condition
        weather_data["weather_icon"] = weather_icon

    return render_template(
        "results.html",
        places_data=places_data,
        events_data=events_data,
        weather_data=weather_data,
        sunrise_time=sunrise_time,
        sunset_time=sunset_time,
        golden_hour_time = golden_hour_time,
        lon=lon,
        lat=lat,
    )


if __name__ == "__main__":
    app.run(debug=True)
