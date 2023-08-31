# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)
inspector = inspect(engine)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

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
        f"/api/v1.0/precipitation>"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs>"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )
@app.route("/api/v1.0/precipitation")
def precipitation():
    prcp_results = session.query(measurement.date, measurement.prcp) \
    .filter(measurement.date >= '2016-08-23')\
    .all()

    prcp_list = []
    for date, prcp in prcp_results:
        prcp_list[date] = prcp
    return jsonify(prcp_list)

@app.route("/api/v1.0/stations")
def stations():
    station_results = session.query(station.station)
    station_list=list(np.ravel(station_results))
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    tobs_results = session.query(measurement.date, measurement.tobs) \
        .filter(measurement.station == "USC00519281") \
        .filter(measurement.date >= "2017-08-23") \
        .all()
    
    tobs_list = []
    for date, tobs in tobs_results:
        tobs_list.append({"date": date, "tobs": tobs})
    
    # Return the JSON list of temperature observations
    return jsonify(tobs_list)


# @app.route("/api/v1.0/<start>")
# def start():

# @app.route("/api/v1.0/<start>/<end>")
# def end():


if __name__ == '__main__':
    app.run(debug=False)