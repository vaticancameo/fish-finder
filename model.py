from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import sqlalchemy

db = SQLAlchemy()


class Station(db.Model):
    """ Table to store station names and locations """

    __tablename__ = "stations"

    station_id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    tides = db.relationship("Tide")
    # tide_details = db.relationship("TideDetail")


class Tide(db.Model):
    """ Table to store tide and station data on a given day """

    __tablename__ = "tides"

    tide_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    station_id = db.Column(db.Integer, db.ForeignKey('stations.station_id'), nullable=False)
    date = db.Column(sqlalchemy.types.Date)
    full_moon = db.Column(db.Boolean)
    sunrise = db.Column(sqlalchemy.types.Time)
    sunset = db.Column(sqlalchemy.types.Time)

    station = db.relationship("Station")
    tide_details = db.relationship("TideDetail")


class TideDetail(db.Model):
    """ Table to store tide details for each Tide ID """

    __tablename__ = "tide_details"

    tide_detail_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    tide_id = db.Column(db.Integer, db.ForeignKey('tides.tide_id'), nullable=False)
    tide_time = db.Column(sqlalchemy.types.Time, nullable=False)
    tide_height = db.Column(db.Float, nullable=False)

    tide = db.relationship("Tide")


###############################
def connect_to_db(app):
    """Connect the database to the Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///fish_finder'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    app = Flask(__name__)
    connect_to_db(app)
    print "Connected to DB."
