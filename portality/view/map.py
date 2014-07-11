__author__ = 'steve'

import json
from flask import Blueprint, request, render_template, make_response

""" show geoip data on an interactive map """

blueprint = Blueprint('map', __name__)

@blueprint.route('/')
def index():
    return render_template('map/index.html')