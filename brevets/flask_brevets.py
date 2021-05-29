"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)

"""

import flask
from flask import Flask, redirect, url_for, request, render_template
import arrow  # Replacement for datetime, based on moment.js
import acp_times  # Brevet time calculations
import config

import logging
import os
from pymongo import MongoClient

###
# Globals
###
app = flask.Flask(__name__)
CONFIG = config.configuration()


client = MongoClient(os.environ['MONGODB_HOSTNAME'])
db = client.tododb

###
# Pages
###


@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    return flask.render_template('404.html'), 404


###############
#
# AJAX request handlers
#   These return JSON, rather than rendering pages.
#
###############
@app.route("/_calc_times")
def _calc_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects one URL-encoded argument, the number of miles.
    """
    app.logger.debug("Got a JSON request")
    km = request.args.get('km', 999, type=float)
    app.logger.debug("km={}".format(km))
    app.logger.debug("request.args: {}".format(request.args))
    maxkm = request.args.get('maxkm', type=int)
    app.logger.debug("maxkm={}".format(maxkm))
    app.logger.debug("request.args: {}".format(request.args))
    date_time = request.args.get('date_time')
    # FIXME: These probably aren't the right open and close times
    # and brevets may be longer than 200km
    open_time = acp_times.open_time(km, maxkm, date_time)
    close_time = acp_times.close_time(km, maxkm, date_time)
    result = {"open": open_time, "close": close_time}
    return flask.jsonify(result=result)

@app.route('/submit', methods=['POST'])
def new():
    #
    db.tododb.delete_many({})

    distance = request.form['distance']
    begin_date = request.form['begin_date']
    begin_time = request.form['begin_time']
    miles_list = request.form.getlist('miles')
    km_list = request.form.getlist('km')
    loc_list = request.form.getlist('location')
    open_list = request.form.getlist('open')
    close_list = request.form.getlist('close')
    item_doc = {
        'distance': distance,
        'begin_date': begin_date,
        'begin_time': begin_time
    }
    db.tododb.insert_one(item_doc)
    for i in range(len(km_list)):
        if (km_list[i] != "" and km_list[i] != None):
            item_doc = {
                'miles': float(miles_list[i]),
                'km': float(km_list[i]),
                'location': loc_list[i],
                'open': open_list[i],
                'close': close_list[i]
            }
            db.tododb.insert_one(item_doc)

    return redirect(url_for('index'))

@app.route('/display')
def display():
    _dist_date_time = db.tododb.find({}, { "distance": 1, "begin_date": 1, "begin_time": 1})
    dist_date_time = []
    i = 0
    for ddt in _dist_date_time:
        if i == 0:
            dist_date_time.append(ddt)
        i += 1
    _items = db.tododb.find({}, { "distance": 0, "begin_date": 0, "begin_time": 0}).sort("km")
    items = []
    i = 0
    for item in _items:
        if i > 0:
            items.append(item)
        i += 1
    return render_template('display.html', dist_date_time=dist_date_time, items=items)


#############

app.debug = CONFIG.DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")
