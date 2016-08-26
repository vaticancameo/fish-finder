from flask import Flask, request, render_template, jsonify
from flask_debugtoolbar import DebugToolbarExtension
import json
import os
from geopy.distance import distance
from datetime import datetime

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

    return render_template("search.html")


@app.route("/", methods=['POST'])
def calculate_distance():
    """ Display distance between origin and destinations """

    # from userInput
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
    result = {"nearest_stations": nearest_stations}

    return jsonify(result)


@app.route("/tides", methods=['POST'])
def display_graph():
    """ Display tide details graph for specific day """

    d = request.form.get("date")
    print "d", d
    # will eventually calculate user-inputted date
    today = datetime.now().date()
    year = today.year
    month = today.month
    day = today.day

    tide_day = TideDay.query.filter(TideDay.station_id == 9414958, TideDay.date == today).all()
    times_heights = TideDetail.query.filter(TideDetail.tide_day_id == tide_day[0].tide_day_id).all()

    print "tide_day", tide_day[0].date
    print "times_heights", times_heights
    print "time mins", times_heights[0].tide_time.minute

    ### NEED TO SUBTRACT ONE FROM MONTH BECAUSE JAN == 0!!!!!
    data = []
    for i in range(len(times_heights)):
        hour = times_heights[i].tide_time.hour
        minute = times_heights[i].tide_time.minute
        height = times_heights[i].tide_height
        time_height = ['Date.UTC({}, {}, {}, {}, {}), {}]'.format(year, month, day, hour, minute, height)]
        data.append(time_height)
    print data

    result = {"high_charts_date": data}
    print "result", result

    return jsonify(result)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
