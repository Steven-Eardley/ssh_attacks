__author__ = 'steve'
"""
Find some other interesting information not written to the logs, and add these to the entry.
"""
from portality.core import app
from pygeoip import GeoIP
from random import randint
from ipwhois import IPWhois

geoip = GeoIP(app.config['GEOIP_PATH'])

def lookup_location(attack_model):
    ip = attack_model.data['attack_ip']
    return geoip.record_by_addr(ip)

def lookup_whois(attack_model):
    from portality.models import NameAndShameEntry
    ip = attack_model.data['attack_ip']

    # Attempt to find a stored name
    name_query = NameAndShameEntry.query(q={"query":{"match":{'id':ip}}})
    print(ip)

    # If we don't find the IP in our index, run whois and create it
    n_matches = name_query['hits']['total']
    if n_matches == 0:
        perp_name = run_whois(ip)
        perp_entry = NameAndShameEntry(id=ip)
        perp_entry.set_perp_name(perp_name)
        perp_entry.save()
        return perp_name
    elif n_matches == 1:
        name_from_index = name_query['hits']['hits'][0]['_source']['perp_name']
        return name_from_index
    else:
        print("Too many results returned for IP {0}. Check or rebuild index.".format(ip))
        exit(1)

def run_whois(ip):
    who = IPWhois(ip).lookup(inc_raw=True)

    # The IPWhois package doesn't give us the name information, so we parse the raw information.
    raw_whois = who['raw']

    return randint(0, 10000)


