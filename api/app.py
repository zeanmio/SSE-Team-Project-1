from flask import Flask, render_template, request, jsonify, redirect, url_for
import requests


app = Flask(__name__)


API_KEYS = {"opentripmap": "5ae2e3f221c38a28845f05b6f0cdf9cd4ed80f90f5ddfc9ebf916642"}
# Add new API keys in the brackets above, separated by commas


BASE_URLS = {"opentripmap": "https://api.opentripmap.com"}
# Add new base URLs in the brackets above, separated by commas


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


# Add new functions here


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

    places_data, error = get_places_data(city)
    if error:
        return jsonify({"error": error}), 500

    # Add new API calls here
    # Get the coordinates of the first place
    lon = places_data.features[0].geometry.coordinates[0]
    lat = places_data.features[0].geometry.coordinates[1]

    return render_template("results.html", places_data=places_data, lon=lon, lat=lat)
    # Add new data in the return function


if __name__ == "__main__":
    app.run(debug=True)
