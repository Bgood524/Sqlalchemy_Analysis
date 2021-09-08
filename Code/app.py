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

@app.route("/jsonified")
def jsonified():
    return jsonify(hello_dict)


if __name__ == "__main__":
    app.run(debug=True)
