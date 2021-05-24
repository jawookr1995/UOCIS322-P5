"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)

"""

import flask
from flask import Flask, redirect, url_for, request, render_template
import arrow  # Replacement for datetime, based on moment.js
import acp_times  # Brevet time calculations
import config
import dbclass # Class variable for database

import logging
import os
from pymongo import MongoClient

###
# Globals
###
app = flask.Flask(__name__)
CONFIG = config.configuration()
app.secret_key = CONFIG.SECRET_KEY


client = dbclass.Mongo(os.environ['MONGODB_HOSTNAME'])
client.connect()
client.mk_db("brevetsdb")



@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    flask.session['linkback'] = flask.url_for("index")
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
    data = request.form.to_dict()
    # Change the data to a list
    data['table'] = eval(data['table'])
    table = data['table']
    # get the most recent submission
    client.delete_all("mostrecent")

    for i in range(len(table)):
        row = table[str(i)]
        client.insert_o("mostrecent", row)
    return flask.jsonify(output=str(data))

@app.route('/display')
def display():
    everything = client.list_all("mostrecent")
    app.logger.debug(everything)
    brevet = begin_date = ""
    if len(everything) > 0:
        brevet = everything[0]['brevet']
        begin_date = everything[0]['begin']
    return flask.render_template('display.html', result=everything, brevet=brevet, begin=begin_date)


#############

app.debug = CONFIG.DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")
