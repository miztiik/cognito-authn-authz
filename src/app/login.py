# -*- coding: utf-8 -*-
__author__ = 'Mystique'
"""
.. module: Serverless Login Page
    :platform: AWS
    :copyright: (c) 2019 Mystique.,
.. moduleauthor:: Mystique
.. contactauthor:: miztiik@github issues
"""

from flask import Flask, render_template, request, redirect, url_for, request
from flask_cors import CORS
import os
import logging

# Initialize Logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

application = Flask(__name__, static_url_path='/static')
application.debug = os.environ.get('DEBUG_MODE', False)
CORS(application)

@application.route("/", methods=['GET', 'POST'])
def login():
   return render_template('login.html')

@application.route('/get_weather_report', methods=['POST', 'GET'])
def get_weather_report():
    """
    Get the weather report from the controller and render them using the models.
    """
    if request.method == 'POST':
        data = request.json
        input_location = data['location']
        w_report = weather_report_controller()
        
        geo_location = w_report.get_location(input_location)
        if geo_location == None:
            wr_address = "Unknown location"
            wr_template = render_template('reports.html', weather_address = wr_address)
            return wr_template 
       
        wr_address = geo_location.address
        w_reports = w_report.get_weather_reports(data, geo_location)

        # Setup crude error handling.
        if w_reports == None:
            w_reports ={'w_report':{'summary':"Unable to fetch weather data from API Service. Check API Key/Logs"}}

        wr_template = render_template('reports.html', weather_address = wr_address, weather_reports = w_reports)

    return wr_template  

def lambda_handler(event, context):
    # application.run( host = '0.0.0.0', port = 80 )
    application.run( host = '0.0.0.0' )