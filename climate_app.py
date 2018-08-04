from flask import Flask, jsonify, render_template
import json
import requests
from flask import request
import sqlalchemy
from sqlalchemy import create_engine, func

from database import session, Measurement, Station, engine


app = Flask(__name__)


@app.route('/')
def home_route():
    return "Hello World"


@app.route('/api/v1.0/precipitation/')
def precip():
    precipitation= session.query(Measurement.date,
                    Measurement.prcp)\
            .filter(Measurement.date>2017)\
            .order_by(Measurement.date.desc())
    dict_values = {d:t for d,t in precipitation}
    return jsonify(dict_values)


@app.route('/api/v1.0/stations')
def station_list():
    stations = []

    for row in session.query(Station):
        stations.append(
            {'id':row.station,
            'name': row.name}
        )
    return jsonify(stations)


@app.route('/api/v1.0/tobs')
def tobs():
    tobs_analysis = session.query(Measurement.date,
                        Measurement.tobs)\
            .filter(Measurement.date>2017)\
            .order_by(Measurement.date.desc())
    dict_val = {x:y for x,y in tobs_analysis}
    return jsonify(dict_val)


@app.route('/api/v1.0/<start>/<end>')
def dates(start,end):
    tobs_date = session.query(
        func.min(Measurement.tobs.label('min_temp')),
        func.max(Measurement.tobs.label('max_temp')),
        func.avg(Measurement.tobs.label('avg_temp')), 
        Measurement.date)\
        .filter(Measurement.date.between('{}'.format(start),'{}'.format(end)))
    return jsonify ({"temperature_data": [x for x in tobs_date][0]})


app.run(debug=True)

