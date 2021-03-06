"""Utility file to seed database with NOAA tide prediction data"""

from sqlalchemy import func
from model import Station, TideDay, TideDetail

from model import connect_to_db, db
from server import app

stations = [9410170, 9410230, 9410580, 9410680, 9410660, 9410840, 9411340,
            9411399, 9411406, 9412110, 9412802, 9413450, 9413663, 9414131,
            9414290, 9414317, 9414764, 9414750, 9414746, 9414358, 9414688,
            9414458, 9414523, 9414509, 9414575, 9414863, 9415218, 9415143,
            9415102, 9415265, 9415144, 9414811, 9415112, 9415064, 9415316,
            9415056, 9415338, 9414958, 9415020, 9416409, 9416841, 9417426,
            9418767, 9418723, 9418817, 9419750, 9419945]


def load_stations():
    """Load stations from u.station into database."""

    print "Stations"

    # Delete all rows in table, so if this is run more than once, duplicate
    # stations will not be added
    Station.query.delete()

    # Read station file and insert data
    for row in open("seed_data/station.txt", 'r'):
        row = row.rstrip()
        station_id, name, latitude, longitude = row.split("\t")

        station = Station(station_id=station_id, name=name, latitude=latitude, longitude=longitude)

        # Add each station to the session
        db.session.add(station)

    # Commit all new stations to the db
    db.session.commit()


def load_tides():
    """Load tide days from [station#].txt into database."""

    print "Tides"

    # Delete all rows in tables, so if this is run more than once, duplicate
    # tides will not be added
    TideDay.query.delete()
    TideDetail.query.delete()

    # Read [station#].txt file and insert data

    for station in stations:
        with open(("seed_data/" + str(station) + '.txt'), 'r') as f:

            for row in f:
                row = row.rstrip()
                current_row = row.split()

                date = current_row.pop(0)

                tide_day = TideDay(station_id=station, date=date)
                db.session.add(tide_day)
                db.session.commit()

                for i in range(0, len(current_row) - 2, 3):
                    tide_detail = TideDetail(tide_day_id=tide_day.tide_day_id, tide_time=current_row[i], tide_height=current_row[i + 1])
                    db.session.add(tide_detail)

        db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.drop_all()
    db.create_all()

    # Import different types of data
    load_stations()
    load_tides()
