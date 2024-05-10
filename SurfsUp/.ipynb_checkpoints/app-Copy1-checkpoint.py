# Import the dependencies.

from flask import Flask, jsonify
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB

session = Session(engine)
#################################################
# Flask Setup
#################################################

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
def prec():
    session = Session(engine)
    previous_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= previous_date).all()
    session.close()
    empty_list = []
    for date, prcp in results:
        list_dict = {}
        list_dict["date"] = date
        list_dict["prcp"] = prcp
        empty_list.append(list_dict)
    return jsonify(empty_list)

@app.route("/api/v1.0/stations")
def stat():
    session = Session(engine)
    results = session.query(station.station).all()
    session.close()
    return jsonify(list(np.ravel(results)))

@app.route("/api/v1.0/tobs")
def tob():
    session = Session(engine)
    previous_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(measurement.date, measurement.tobs).\
        filter(measurement.station == "USC00519281").\
        filter(measurement.date >= previous_date).all()
    session.close()
    results = list(np.ravel(results))
    return jsonify(results)

@app.route("/api/v1.0/temp/<start>/<end>")
def stat(start, end):
    session = Session(engine)
    start = dt.datetime.strptime(start, "%Y-%m-%d").date()
    end = dt.datetime.strptime(end, "%Y-%m-%d").date()
    sel = [
        func.min(Measurment.tobs),
        func.avg(Measurment.tobs),
        func.max(Measurment.tobs),
    ]
    results = (
        session.query(*sel)
        .filter(Measurment.date >= start)
        .filter(Measurment.date <= end)
        .all()
    )
    session.close()
    temp_list = []
    for result in results:
        temp_dict = {}
        (temp_min, temp_avg, temp_max) = result
        temp_dict["minimum_temp"] = temp_min
        temp_dict["maximum_temp"] = temp_max
        temp_dict["average_temp"] = temp_avg
        temp_list.append(temp_dict)
    return jsonify(temp_list)

if __name__ == "__main__":
    app.run(debug=True)


#################################################
# Flask Routes
#################################################
