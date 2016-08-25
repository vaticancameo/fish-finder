from flask import Flask, request, render_template, jsonify
from flask_debugtoolbar import DebugToolbarExtension
import json
import os
from geopy.distance import distance

from model import connect_to_db
from model import Station, TideDay, TideDetail

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# key = os.environ['GOOGLE_MAPS_API_KEY']

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"


@app.route("/")
def display_map():
    """ Display map with search box and test markers """

    station1 = {"id": "9414958", "name": "Bolinas, Bolinas Lagoon", "lat": 37.9080, "lon": -122.6785}
    station2 = {"id": "9410170", "name": "San Diego", "lat": 32.7142, "lon": -117.1736}

    stations_locations = [station1, station2]

    stations_locations_str = json.dumps(stations_locations)

    return render_template("search.html", data=stations_locations_str)


@app.route("/", methods=['POST'])
def calculate_distance():
    """ Display distance between origin and destinations """

    lat = request.form.get("lat")
    lon = request.form.get("lon")

    all_stations = Station.query.all()

    station_distances = []

    for station in all_stations:
        slat = station.latitude
        slon = station.longitude
        dist = distance((lat, lon), (slat, slon)).miles

        station_distances.append({"name": station.name, "lat": station.latitude, "lng": station.longitude, "dist": dist})

    nearest_stations = sorted(station_distances, key=lambda d: d["dist"])[:7]
    print "nearest stations: ", nearest_stations

    # lats_lons = []
    # for station in nearest_stations:
    #     lat_lng = {k: station[k] for k in ('lat', 'lng')}
    #     lats_lons.append(lat_lng)

    # print "lats_lons: ", lats_lons
    result = {"nearest_stations": nearest_stations}
    return jsonify(result)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
