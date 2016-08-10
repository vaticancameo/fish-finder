from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Cat(db.Model):
    """table to store cats"""
    
    __tablename__ = 'cats'

    cat_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(64))
    age = db.Column(db.Integer, nullable=True)

    boxes = db.relationship("LitterBox",
                             secondary="catslitterboxes")

class LitterBox(db.Model):
    """table to store places for cats to do their business"""

    __tablename__ = "litterboxes"

    litter_box_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    location = db.Column(db.String(32), nullable=False)
    needs_litter = db.Column(db.Boolean, default=False)
    needs_cleaning = db.Column(db.Boolean, default=False)

    cats = db.relationship("Cat",
                            secondary="catslitterboxes")

class CatLitterBox(db.Model):

    __tablename__ = "catslitterboxes"

    catbox_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    cat_id = db.Column(db.Integer, db.ForeignKey("cats.cat_id"))
    box_id = db.Column(db.Integer, db.ForeignKey("litterboxes.litter_box_id"))


###############################
def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cat_review'
    db.app = app
    db.init_app(app)


def create_example_data():

    db.drop_all()
    db.create_all()

    # make some cats
    cisco = Cat(name='Cisco', age=17)
    young_fluffy = Cat(name='fluffy', age=2)
    old_fluffy = Cat(name='fluffy', age=23)
    db.session.add_all([cisco, young_fluffy, old_fluffy])

    # make some litter boxes
    upstairs_bath = LitterBox(location="upstairs bath")
    downstairs_bath = LitterBox(location="downstairs bath")
    kitchen = LitterBox(location="kitchen")
    db.session.add_all([upstairs_bath, downstairs_bath, kitchen])

    # make some preferences
    cisco.boxes.extend([upstairs_bath, downstairs_bath])
    young_fluffy.boxes.extend([upstairs_bath, downstairs_bath, kitchen])
    old_fluffy.boxes.append(downstairs_bath)

    db.session.commit()


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    app = Flask(__name__)
    connect_to_db(app)
    create_example_data()
    print "Connected to DB."
