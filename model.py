from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Station(db.Model):
    """ Table to store station names and locations """

    __tablename__ = "stations"

    station_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    tides = db.relationship("Tide")


class Tide(db.Model):
    """ Table to store tide data for each station on a given day """

    __tablename__ = "tides"

    tide_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    station_id = db.Column(db.Integer, db.ForeignKey('stations.station_id'), nullable=False)

    stations = db.relationship("Station")


###############################
def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///stations_tides'
    db.app = app
    db.init_app(app)


def create_example_data():

    db.drop_all()
    db.create_all()

    # # make some cats
    # cisco = Cat(name='Cisco', age=17)
    # young_fluffy = Cat(name='fluffy', age=2)
    # old_fluffy = Cat(name='fluffy', age=23)
    # db.session.add_all([cisco, young_fluffy, old_fluffy])

    # # make some litter boxes
    # upstairs_bath = LitterBox(location="upstairs bath")
    # downstairs_bath = LitterBox(location="downstairs bath")
    # kitchen = LitterBox(location="kitchen")
    # db.session.add_all([upstairs_bath, downstairs_bath, kitchen])

    # # make some preferences
    # cisco.boxes.extend([upstairs_bath, downstairs_bath])
    # young_fluffy.boxes.extend([upstairs_bath, downstairs_bath, kitchen])
    # old_fluffy.boxes.append(downstairs_bath)

    db.session.commit()


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    app = Flask(__name__)
    connect_to_db(app)
    create_example_data()
    print "Connected to DB."
