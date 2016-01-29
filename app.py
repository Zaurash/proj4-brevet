"""
Very simple Flask web site, with one page
displaying a course schedule.

"""

import flask
from flask import render_template
from flask import request
from flask import url_for
from flask import jsonify # For AJAX transactions
from math import modf

import json
import logging

# Date handling 
import arrow # Replacement for datetime, based on moment.js
import datetime # But we still need time
from dateutil import tz  # For interpreting local times

# Our own module
# import acp_limits


###
# Globals
###
app = flask.Flask(__name__)
import CONFIG

import uuid
app.secret_key = str(uuid.uuid4())
app.debug=CONFIG.DEBUG
app.logger.setLevel(logging.DEBUG)


###
# Pages
###

@app.route("/")
@app.route("/index")
@app.route("/calc")
def index():
  app.logger.debug("Main page entry")
  return flask.render_template('calc.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    flask.session['linkback'] =  flask.url_for("calc")
    return flask.render_template('page_not_found.html'), 404


###############
#
# AJAX request handlers 
#   These return JSON, rather than rendering pages. 
#
###############
@app.route("/_calc_times")
def calc_times():
  """
  Calculates open/close times from kms, using rules 
  described at http://www.rusa.org/octime_alg.html.
  Expects one URL-encoded argument, the number of kms. 
  """
  app.logger.debug("Got a JSON request");
  kms = request.args.get('kms', 0, type=int)
  if(kms < 0):
      return jsonify(result="Distance cannot be negative")
  elif(kms <= 200):
      hour = stepstone(kms, 34)[0]
      minutes = stepstone(kms, 34)[1]
      opening = "Opening time: " + str(hour) + ":" + str(minutes) + " "
      hourc = stepstone(kms, 15)[0]
      minutesc = stepstone(kms, 15)[1]
      closing = "Closing time: " + str(hourc) + ":" + str(minutesc)
  elif(kms <= 400):
      hour = stepstone(kms, 32)[0]
      minutes = stepstone(kms, 32)[1]
      opening = "Opening time: " + str(hour) + ":" + str(minutes) + " "
      hourc = stepstone(kms, 15)[0]
      minutesc = stepstone(kms, 15)[1]
      closing = "Closing time: " + str(hourc) + ":" + str(minutesc)
  elif(kms <= 600):
      hour = stepstone(kms, 30)[0]
      minutes = stepstone(kms, 30)[1]
      opening = "Opening time: " + str(hour) + ":" + str(minutes) + " "
      hourc = stepstone(kms, 15)[0]
      minutesc = stepstone(kms, 15)[1]
      closing = "Closing time: " + str(hourc) + ":" + str(minutesc)
  elif(kms <= 1000):
      hour = stepstone(kms, 26)[0]
      minutes = stepstone(kms, 26)[1]
      opening = "Opening time: " + str(hour) + ":" + str(minutes) + " "
      hourc = stepstone(kms, 11.428)[0]
      minutesc = stepstone(kms, 11.428)[1]
      closing = "Closing time: " + str(hourc) + ":" + str(minutesc)
  elif(kms <= 1300):
      hour = stepstone(kms, 26)[0]
      minutes = stepstone(kms, 26)[1]
      opening = "Opening time: " + str(hour) + ":" + str(minutes) + " "
      hourc = stepstone(kms, 13.333)[0]
      minutesc = stepstone(kms, 13.333)[1]
      closing = "Closing time: " + str(hourc) + ":" + str(minutesc)
  else:
      return jsonify(result="Distance must be under 1300 Kilometers")
  final = opening + closing
  return jsonify(result=final)
 
#################
#
# Functions used within the templates
#
#################

def stepstone(dist, rate):
    hour = int(modf(dist / rate)[1])
    minutes = int(modf(dist / rate)[0] * 60)
    return [hour, minutes]

@app.template_filter( 'fmtdate' )
def format_arrow_date( date ):
    try: 
        normal = arrow.get( date )
        return normal.format("ddd MM/DD/YYYY")
    except:
        return "(bad date)"

@app.template_filter( 'fmttime' )
def format_arrow_time( time ):
    try: 
        normal = arrow.get( date )
        return normal.format("hh:mm")
    except:
        return "(bad time)"



#############


if __name__ == "__main__":
    import uuid
    app.secret_key = str(uuid.uuid4())
    app.debug=CONFIG.DEBUG
    app.logger.setLevel(logging.DEBUG)
    app.run(port=CONFIG.PORT)

    
