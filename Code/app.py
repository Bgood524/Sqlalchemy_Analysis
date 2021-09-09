import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import datetime as dt

app = Flask(__name__)

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station

@app.route("/")
def home():
    """List all available api routes."""
    return ("""
        Available Routes:<br/>
        /api/v1.0/precipitation<br/>
        /api/v1.0/stations<br/>
        /api/v1.0/start<br/>
        /api/v1.0/tobs<br/>
        /api/v1.0/start/end<br/>
    """)



@app.route("/api/v1.0/precipitation")
def prcp():      
    session = Session(engine)
    recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).all()
    string_date = recent_date[0][0].split('-')
    year = int(string_date[0])
    month = int(string_date[1])
    day = int(string_date[2])
    first_date =dt.date(year,month,day)
    first_date
    last_date = first_date - dt.timedelta(days=365)
    last_date
    twelve_months = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= last_date).all()
    prcp_data = {}
    for row in twelve_months:
        date = row[0]
        prcp = row[1]
        prcp_data[date] = prcp
    session.close() 
    return jsonify(prcp_data)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    rows = session.query(Station.station).all()
    session.close()
    station_data = list(np.ravel(rows))
    return jsonify(station_data=station_data)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    last_date = dt.date(2017,8,23) - dt.timedelta(days=365)
    tobs_data = session.query(Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= last_date).all()
    session.close()
    tobs_jsonify = list(np.ravel(tobs_data=tobs_data))
    return jsonify(tobs_jsonify)

@app.route("/api/v1.0/<start>")
def start(start):
    session = Session(engine)
    start = dt.datetime.strptime(start,'%m/%d/%Y')
    temp_data = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).all()
    session.close()
    temp_data_jsonify = list(np.ravel(temp_data=temp_data))
    return jsonify(temp_data_jsonify)



if __name__ == "__main__":
    app.run(debug=True)
