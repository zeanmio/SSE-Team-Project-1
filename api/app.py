from flask import Flask, render_template, request, jsonify, redirect, url_for
import requests


app = Flask(__name__)


API_KEYS = {"opentripmap": "5ae2e3f221c38a28845f05b6f0cdf9cd4ed80f90f5ddfc9ebf916642"}


SEATGEEK_CLIENT_ID = 'Mzg2MDA4NDd8MTcwMTI1MzQ0Mi42NzI0ODE4'


SEATGEEK_CLIENT_SECRET = '42ab0a3837f94f19b3bdcf5f0ba4192c5c399491e49bcb78dd39852ab61c698b'


BASE_URLS = {"opentripmap": "https://api.opentripmap.com"}


def get_seatgeek_events(city, date):
    base_url = "https://api.seatgeek.com/2/events"
    params = {
        'client_id': SEATGEEK_CLIENT_ID,
        'client_secret': SEATGEEK_CLIENT_SECRET,
        'venue.city': city,
        'datetime_local.gte': date,  # Assuming you want events from this date forward
        'datetime_local.lte': date   # If you want events only on this date, set this too
    }
    response = requests.get(base_url, params=params)
    if response.ok:
        return response.json(), None
    else:
        return None, "Error fetching events from SeatGeek"


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


    places_data, places_error = get_places_data(city)
    events_data, events_error = get_seatgeek_events(city, date)

    if places_error or events_error:
        error_message = places_error or events_error
        return jsonify({"error": error_message}), 500

    
    return render_template("results.html", places_data=places_data, events_data=events_data['events'])


if __name__ == "__main__":
    app.run(debug=True)
