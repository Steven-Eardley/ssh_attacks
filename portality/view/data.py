__author__ = 'steve'

import json
from flask import Blueprint, render_template
from portality import models

""" preview the data in the index """

blueprint = Blueprint('data', __name__)

@blueprint.route('/')
def index():
    data_aggs =\
    {
        "size" : 0,
        "aggregations" :
        {
        "name_count" :
            {
                "terms" :
                {
                    "field" : "attack_name"
                }
            },
        "ip_count" :
            {
                "terms" :
                {
                    "field" : "attack_ip"
                }
            }
        }
    }

    agg_results = models.SshEntry.query(q=data_aggs)

    # Collect the data lists from the aggregations
    name_results = agg_results['aggregations']['name_count']['buckets']
    ip_results = agg_results['aggregations']['ip_count']['buckets']

    # Pick out some top results to insert into text.
    top_name = agg_results['aggregations']['name_count']['buckets'][0]['key']
    top_name_freq = agg_results['aggregations']['name_count']['buckets'][0]['doc_count']

    return render_template('data/preview.html',top_name=top_name, top_name_freq=top_name_freq, data_name=name_results, data_ip=ip_results)
