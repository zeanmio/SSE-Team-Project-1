from flask import Flask, render_template, request, jsonify, redirect, url_for
import requests


app = Flask(__name__)


API_KEYS = {"opentripmap": "5ae2e3f221c38a28845f05b6f0cdf9cd4ed80f90f5ddfc9ebf916642",
            "openweather": "1d3ffd302d0bd84b18314ffbc3d10669"}


BASE_URLS = {"opentripmap": "https://api.opentripmap.com",
            "openweather": "https://api.openweathermap.org"}


def get_places_data(city):
    geoname_url = f"{BASE_URLS['opentripmap']}/0.1/en/places/geoname?name={city}&apikey={API_KEYS['opentripmap']}"
    geoname_response = requests.get(geoname_url)

    if not geoname_response.ok:
        return None, "Error fetching geoname data"

    geoname_data = geoname_response.json()
    lon = geoname_data["lon"]
    lat = geoname_data["lat"]

    places_url = f"{BASE_URLS['opentripmap']}/0.1/en/places/radius?radius=1000&lon={lon}&lat={lat}&rate=3h&limit=20&apikey={API_KEYS['opentripmap']}"
    places_response = requests.get(places_url)

    if not places_response.ok:
        return None, "Error fetching places"

    return places_response.json(), None

def get_weather_data(lat, lon, date):
    weather_url = f"{BASE_URLS['openweather']}/data/3.0/onecall/day_summary?lat={lat}&lon={lon}&date={date}&appid={API_KEYS['openweather']}"
    response = requests.get(weather_url)
    print("Request URL:", weather_url)

    response = requests.get(weather_url)
    print("Response:", response.text)

    if not response.ok:
        return None, "Error fetching weather data"
    return response.json(), None


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

    print("All request parameters:", request.args)

    places_data, error = get_places_data(city)
    if error:
        return jsonify({"error": error}), 500

    # Extract latitude and longitude from places_data
    if places_data and "features" in places_data:
        location = places_data["features"][0]["geometry"]["coordinates"]
        lat, lon = location[1], location[0]

        # Get weather data
        weather_data, weather_error = get_weather_data(lat, lon, date)
        if weather_error:
            return jsonify({"error": weather_error}), 500

        # Extract min and max temperatures from weather_data
        min_temp = round (weather_data["temperature"]["min"] - 273.15)
        max_temp = round (weather_data["temperature"]["max"] - 273.15)
        
        print (min_temp)

    return render_template("results.html", places_data=places_data, min_temp=min_temp, max_temp=max_temp)


if __name__ == "__main__":
    app.run(debug=True)
