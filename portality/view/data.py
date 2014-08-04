__author__ = 'steve'

import json
from flask import Blueprint, render_template
from portality import models

""" preview the data in the index """

blueprint = Blueprint('data', __name__)

@blueprint.route('/')
def index():
    count_names_query =\
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
            }
       }
    }

    names = models.SshEntry.query(q=count_names_query)
    count_results = (names['aggregations']['name_count']['buckets'])
    print(count_results)
    return render_template('data/preview.html', data=count_results)
