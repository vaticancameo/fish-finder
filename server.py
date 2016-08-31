# Note: I will clear out the imports I am not using next week:
from flask import Flask, request, render_template, jsonify
from flask_debugtoolbar import DebugToolbarExtension
import json
import os
from geopy.distance import distance
from datetime import datetime
from dateutil import tz
import pytz
from model import connect_to_db
from model import Station, TideDay, TideDetail

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

key = os.environ['GOOGLE_MAPS_API_KEY']

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"


@app.route("/")
def display_map():
    """ Display map with search box and test markers """

    return render_template("search.html")


@app.route("/", methods=['POST'])
def calculate_distance():
    """ Calculate distances of 7 closest latitudes/longitudes to user's search location """

    # from userInput
    lat = request.form.get("lat")
    lon = request.form.get("lon")

    all_stations = Station.query.all()

    station_distances = []

    for station in all_stations:
        slat = station.latitude
        slon = station.longitude
        dist = distance((lat, lon), (slat, slon)).miles

        station_distances.append({"name": station.name, "id": station.station_id, "lat": station.latitude, "lng": station.longitude, "dist": dist})

    nearest_stations = sorted(station_distances, key=lambda d: d["dist"])[:7]
    result = {"nearest_stations": nearest_stations}

    return jsonify(result)


@app.route("/tides", methods=['POST'])
def display_graph():
    """ Display tide details graph for specific day """

    id = request.form.get("id")
    user_date = request.form.get("date")
    s_date = str(user_date)

    # I know this can be condensed, but don't yet have time to do it.  If you can show me
    # the way, I'd appreciate it.
    if s_date:
        date = datetime.strptime(s_date, "%m/%d/%Y")
        tide_day = TideDay.query.filter(TideDay.station_id == id, TideDay.date == date).all()
        year = date.year
        month = date.month
        day = date.day
    else:
        today = datetime.now().date()
        tide_day = TideDay.query.filter(TideDay.station_id == id, TideDay.date == today).all()
        year = today.year
        month = today.month
        day = today.day

    times_heights = TideDetail.query.filter(TideDetail.tide_day_id == tide_day[0].tide_day_id).all()

    # Constructing integer timestamps and heights in the format Highcharts.js is expecting
    data = []
    for i in range(len(times_heights)):
        hour = times_heights[i].tide_time.hour
        minute = times_heights[i].tide_time.minute
        height = times_heights[i].tide_height
        time_height = [int(datetime(year, month, day, hour, minute).strftime('%s')) * 1000, height]
        data.append(time_height)

    return jsonify(data)


if __name__ == "__main__":
    app.debug = True
    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
