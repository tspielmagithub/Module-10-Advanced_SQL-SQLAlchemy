# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
app = Flask(__name__)
#################################################

#################################################
# Flask Routes
#################################################
# Start the main page and show all available routes

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
     f"Welcome to Temperature analysis page!<br/>"
     f"Available Routes:<br/>"
     f"Daily precipitation data for the last 12 months: /api/v1.0/precipitation<br/>"
     f"List of observation stations: /api/v1.0/stations<br/>"
     f"Temperature observations of the most-active station for the previous year:/api/v1.0/tobs<br/>"
     f"<br/>"
     f"Minimum temperature, the average temperature, and the maximum temperature for a specified start:/api/v1.0/<start><br/>"
     f"Put the start date in 'YYYY-MM-DD' format<br/>"
     f"<br/>"
     f"Minimum temperature, the average temperature, and the maximum temperature from the start to the end date:/api/v1.0/<start>/<end><br/>"
     f"Put the dates in 'YYYY-MM-DD/YYYY-MM-DD' format<br/>"
 )

##################################################################


@app.route("/api/v1.0/precipitation")
def prcp():
    # Calculate the dates
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # query only the last 12 months of data
    prcp_all=session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= query_date).all()

    session.close()
    # Create a dictionary from the row data and append to a list
    precipitation = []
    for date, prcp in prcp_all:
        prcp_all_dict = {}
        prcp_all_dict["date"] = date
        prcp_all_dict["prcp"] = prcp
        precipitation.append(prcp_all_dict)
    
    return jsonify(precipitation)

##########################################################################
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # station data
    total_stations = session.query(Station.name).all()
    session.close()
    # Convert list of tuples into normal list
    stations_data = list(np.ravel(total_stations))
    return jsonify(stations_data)


###############################################################################
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Query the dates and temperature observations of the most-active station for the previous year of data
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    year_temp = session.query(Measurement.tobs).\
    filter(Measurement.station == 'USC00519281').\
    filter(Measurement.date >= query_date).all()

    session.close()
    # Convert list of tuples into normal list
    all_year_temp= list(np.ravel(year_temp))

    return jsonify(all_year_temp) 


#######################################################################
### Dynamic routes
@app.route("/api/v1.0/<start>")
def tstart(start):
    """ When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date."""
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
              filter(Measurement.date >= start).order_by(Measurement.date.desc()).all()
    #list = []
    print(f"Temperaturs for the dates greater than or equal to the start date")
    for temps in results:
        dict = {"Minimum Temp":results[0][0],"Average Temp":results[0][1],"Maximum Temp":results[0][2]}
        #list.append(dict)
    return jsonify(dict) 

@app.route("/api/v1.0/<start>/<end>")
def tstartend(start,end):         
    """ When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive. """    
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
                  filter(Measurement.date >= start, Measurement.date <= end).order_by(Measurement.date.desc()).all()
    print(f"Temperaturs for the dates greater than or equal to the start date and lesser than or equal to the end date")
    for temps in results:
        dict = {"Minimum Temp":results[0][0],"Average Temp":results[0][1],"Maximum Temp":results[0][2]}
    return jsonify(dict)   

if __name__ == '__main__':
    app.run(debug=True)