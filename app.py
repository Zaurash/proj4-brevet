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
  
  finalOpen = [0,0]
  finalClose = [0,0]
  closeTimes = []
  openTimes = []
  
  if(kms < 0):
      return jsonify(result="Distance cannot be negative")
  elif(kms <= 200):
      finalOpen = stepstone(kms, 34)
      if kms == 0:
          finalClose = 1
      else:
         finalClose = stepstone(kms, 15) 
      if finalOpen[1] == 60:
          finalOpen[0] += 1
          finalOpen[1] = 0
      if finalOpen[1] > 60:
          finalOpen[0] += finalOpen % 60
          finalOpen[1] = finalOpen // 60
      if finalClose[1] > 60:
          finalClose[0] += finalClose % 60
          finalClose[1] = finalClose // 60
      fullOpen = str(finalOpen[1])
      fullClose = str(finalClose[1])
      if fullOpen == "0":
          fullOpen = "00"
      if fullClose == "0":
          fullClose = "00"
      opening = "Opening time: " + str(finalOpen[0]) + ":" + fullOpen + " "
      closing = "Closing time: " + str(finalClose[0]) + ":" + fullClose 
      
  elif(kms <= 400):
      finalOpen = stepstone(kms, 32)
      finalClose = stepstone(kms, 15) 
      if finalOpen[1] == 60:
          finalOpen[0] += 1
          finalOpen[1] = 0  
      if finalOpen[1] > 60:
          finalOpen[0] += finalOpen % 60
          finalOpen[1] = finalOpen // 60
      if finalClose[1] > 60:
          finalClose[0] += finalClose % 60
          finalClose[1] = finalClose // 60
      fullOpen = str(finalOpen[1])
      fullClose = str(finalClose[1])
      if fullOpen == "0":
          fullOpen = "00"
      if fullClose == "0":
          fullClose = "00"
      opening = "Opening time: " + str(finalOpen[0]) + ":" + fullOpen + " "
      closing = "Closing time: " + str(finalClose[0]) + ":" + fullClose 
      
  elif(kms <= 600):
      finalOpen = stepstone(kms, 30)
      finalClose = stepstone(kms, 15)  
      if finalOpen[1] == 60:
          finalOpen[0] += 1
          finalOpen[1] = 0 
      if finalOpen[1] > 60:
          finalOpen[0] += finalOpen % 60
          finalOpen[1] = finalOpen // 60
      if finalClose[1] > 60:
          finalClose[0] += finalClose % 60
          finalClose[1] = finalClose // 60
      fullOpen = str(finalOpen[1])
      fullClose = str(finalClose[1])
      if fullOpen == "0":
          fullOpen = "00"
      if fullClose == "0":
          fullClose = "00"
      opening = "Opening time: " + str(finalOpen[0]) + ":" + fullOpen + " "
      closing = "Closing time: " + str(finalClose[0]) + ":" + fullClose 
  elif(kms <= 1000):
      finalOpen = stepstone(kms, 28)
      finalClose = stepstone(kms, 11.428)
      if finalOpen[1] == 60:
          finalOpen[0] += 1
          finalOpen[1] = 0   
      if finalOpen[1] > 60:
          finalOpen[0] += finalOpen % 60
          finalOpen[1] = finalOpen // 60
      if finalClose[1] > 60:
          finalClose[0] += finalClose % 60
          finalClose[1] = finalClose // 60
      fullOpen = str(finalOpen[1])
      fullClose = str(finalClose[1])
      if fullOpen == "0":
          fullOpen = "00"
      if fullClose == "0":
          fullClose = "00"
      opening = "Opening time: " + str(finalOpen[0]) + ":" + fullOpen + " "
      closing = "Closing time: " + str(finalClose[0]) + ":" + fullClose 
  elif(kms <= 1300):
      finalOpen = stepstone(kms, 26)
      finalClose = stepstone(kms, 13.333)
      if finalOpen[1] == 60:
          finalOpen[0] += 1
          finalOpen[1] = 0   
      if finalOpen[1] > 60:
          finalOpen[0] += finalOpen % 60
          finalOpen[1] = finalOpen // 60
      if finalClose[1] > 60:
          finalClose[0] += finalClose % 60
          finalClose[1] = finalClose // 60
      fullOpen = str(finalOpen[1])
      fullClose = str(finalClose[1])
      if fullOpen == "0":
          fullOpen = "00"
      if fullClose == "0":
          fullClose = "00"
      opening = "Opening time: " + str(finalOpen[0]) + ":" + fullOpen + " "
      closing = "Closing time: " + str(finalClose[0]) + ":" + fullClose 
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

    
