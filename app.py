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

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Temperature"""
    
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= '2016-08-23').\
        filter(Measurement.date <= '2017-08-23').\
        filter(Measurement.station == 'USC00519281').all()

    session.close()

    all_temp = []
    for date, temp in results:
        temp_dict = {}
        temp_dict[date] = temp
        all_temp.append(temp_dict)

    return jsonify(all_temp)

@app.route("/api/v1.0/<start>")
def temp_start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Temperature Summary"""
    
    if (start <= '2017-08-23'):
        results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
            filter(Measurement.date >= start).all()
        
        all_temp = []
        for min, max, avg in results:
            temp_dict = {}
            temp_dict["min"] = min
            temp_dict["max"] = max
            temp_dict["avg"] = avg
            all_temp.append(temp_dict)
           
        return jsonify(all_temp)
       
    else:
        return jsonify({"error": f"Start date out of range."}), 404   

    session.close()

@app.route("/api/v1.0/<start>/<end>")
def temp_summary(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Temperature Summary"""
    
    if ((start <= '2017-08-23') & (end >= '2010-01-01') & (start < end)):
        results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
            filter(Measurement.date >= start).\
            filter(Measurement.date <= end).all()
        
        all_temp = []
        for min, max, avg in results:
            temp_dict = {}
            temp_dict["min"] = min
            temp_dict["max"] = max
            temp_dict["avg"] = avg
            all_temp.append(temp_dict)
           
        return jsonify(all_temp)
       
    else:
        return jsonify({"error": f"Start or end date out of range."}), 404   

    session.close()

if __name__ == '__main__':
    app.run(debug=True)
