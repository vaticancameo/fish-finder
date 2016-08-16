from flask import Flask, request, render_template
from flask_debugtoolbar import DebugToolbarExtension
import json
import os
from geopy.distance import distance

app = Flask(__name__)

key = os.environ['GOOGLE_MAPS_API_KEY']

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"


@app.route("/")
def display_map():
    """ Display map with search box and test markers """

    station1 = {"id": "9414958", "name": "Bolinas, Bolinas Lagoon", "lat": 37.9080, "lon": -122.6785}
    station2 = {"id": "9414958", "name": "Bolinas, Bolinas Lagoon", "lat": 37.715593, "lon": -122.307468}

    stations_locations = [station1, station2]

    stations_locations_str = json.dumps(stations_locations)

    return render_template("google_maps_api_search.html", data=stations_locations_str, key=key)


@app.route("/distance")
def calculate_distance():
    """ Display distance between origin and destinations """

    return render_template("google_maps_distance_test.html")


@app.route("/test", methods=['POST'])
def test():
   
    lat = request.form.get("lat")
    lon = request.form.get("lon")

    station1 = {"id": "9414958", "name": "Bolinas, Bolinas Lagoon", "lat": 37.9080, "lon": -122.6785}
    station2 = {"id": "9414958", "name": "Bolinas, Bolinas Lagoon", "lat": 37.715593, "lon": -122.307468}

    stations_locations = [station1, station2]
    closest_station = None
    closest_dist = 10000000
    station_distances = []

    for station in stations_locations:
        slat = station["lat"]
        slon = station["lon"]
        dist = distance((lat, lon), (slat, slon)).miles

        station_distances.append({"station": station, "dist": dist})

    nearest_stations = sorted(station_distances, key=lambda d: d["dist"])[:10]

    print nearest_stations

    result = {"nearest_stations": nearest_stations}
    return json.dumps(result)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")