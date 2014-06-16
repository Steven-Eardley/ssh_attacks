__author__ = 'steve'

import json
from flask import Blueprint, request, render_template, make_response

""" preview the data in the index """

blueprint = Blueprint('explorer', __name__)

@blueprint.route('/')
def index():
    return render_template('data/explorer.html')
