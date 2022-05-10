import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Precipitation"""
    
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    all_precipitation = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict[date] = prcp
        all_precipitation.append(precipitation_dict)

    return jsonify(all_precipitation)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Station"""
    
    results = session.query(Station.station, Station.id).all()

    session.close()

    all_stations = []
    for station, id in results:
        station_dict = {}
        station_dict[id] = station
        all_stations.append(station_dict)

    return jsonify(all_stations)


if __name__ == '__main__':
    app.run(debug=True)
