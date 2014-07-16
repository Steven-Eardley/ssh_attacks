__author__ = 'steve'

import json
from flask import Blueprint, request, render_template, make_response
from portality import models
from nltk.probability import FreqDist


""" preview the data in the index """

blueprint = Blueprint('data', __name__)

@blueprint.route('/')
def index():
    entry_query = models.SshEntry.query()
    total_entries = entry_query['hits']['total']

    attacks = models.SshEntry.query(size=total_entries)
    attks = [a['_source'] for a in attacks['hits']['hits']]

    attack_names = [a['attack_name'] for a in attks]
    fdist = FreqDist(attack_names)

    print(fdist)

    #str(attacks['hits']['hits'][0]['_source']['attack_name'])
    return render_template('data/preview.html', data=fdist)
    #resp = make_response(json.dumps(fdist))

    #resp.mimetype = "application/json"
    #return(resp)