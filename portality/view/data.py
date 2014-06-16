__author__ = 'steve'
import json
from flask import Blueprint, request, render_template
from portality import models

""" preview the data in the index """

blueprint = Blueprint('data', __name__)

@blueprint.route('/')
def index():
    attacks = models.SshEntry.query()
    attks = [a['_source']['attack_name'] for a in attacks['hits']['hits']]

    #str(attacks['hits']['hits'][0]['_source']['attack_name'])
    #return render_template('data/preview.html')
    return(str(attks))