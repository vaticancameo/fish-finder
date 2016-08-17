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
    station2 = {"id": "9410170", "name": "San Diego", "lat": 32.7142, "lon": -117.1736}

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
    station2 = {"id": "9410170", "name": "San Diego", "lat": 32.7142, "lon": -117.1736}
    station3 = {"id": "9410230", "name": "La Jolla", "lat": 32.8667, "lon": -117.258}
    station4 = {"id": "9410580", "name": "Newport Bay Entrance", "lat": 33.6033, "lon": -117.883}
    station5 = {"id": "9410680", "name": "Long Beach", "lat": 33.7517, "lon": -118.227}
    station6 = {"id": "9410660", "name": "Los Angeles", "lat": 33.72, "lon": -118.272}
    station7 = {"id": "9410840", "name": "Santa Monica", "lat": 34.0083, "lon": -118.5}
    station8 = {"id": "9411340", "name": "Santa Barbara", "lat": 34.4083, "lon": -119.685}
    station9 = {"id": "9411399", "name": "Gaviota State Park", "lat": 34.4694, "lon": -120.2283}
    station10 = {"id": "9412110", "name": "Port San Luis", "lat": 35.1767, "lon": -120.76}

    stations_locations = [station1, station2, station3, station4, station5, station6, station7, station8, station9, station10]

    station_distances = []

    for station in stations_locations:
        slat = station["lat"]
        slon = station["lon"]
        dist = distance((lat, lon), (slat, slon)).miles

        station_distances.append({"station": station, "dist": dist})

    nearest_stations = sorted(station_distances, key=lambda d: d["dist"])[:7]

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
