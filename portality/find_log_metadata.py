__author__ = 'steve'
"""
Find some other interesting information not written to the logs, and add these to the entry.
Copyright information can be found here: http://www.apnic.net/db/dbcopyright.html, and states:

 " Users will not be able to download the full contents of the database unless the intended use
   is for "Internet operational issues". These words are tightly defined and would include network
   trouble-shooting, abuse reporting, and Internet research and analysis. "

This use falls under 'abuse reporting'.
"""

import re
from portality.core import app
from pygeoip import GeoIP
from random import randint
from ipwhois import IPWhois

geoip = GeoIP(app.config['GEOIP_PATH'])

def lookup_location(attack_model):
    """
    The GeoIP database configured in app.config allows lookup of attacker's location.
    :param attack_model: an SshEntry to add the location to.
    :return: a dict of location information.
    """
    ip = attack_model.data['attack_ip']
    return geoip.record_by_addr(ip)

def lookup_whois(attack_model):
    """
    Find and parse the whois information for an IP address, and store it in an index.
    Each whois takes some time; the index considerably improves speed for repeated attacks
    (plus prevents spamming).
    :param attack_model: an SshEntry to add whois information to
    :return: the name of the attacker
    """
    from portality.models import NameAndShameEntry
    ip = attack_model.data['attack_ip']

    # Attempt to find a stored name
    name_query = NameAndShameEntry.query(q={"query":{"match":{'id':ip}}})

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
    """
    Run the whois, given an IP
    :param ip: string encoded IP address
    :return: the name of the attacker
    """
    who = IPWhois(ip).lookup(inc_raw=True)

    # The IPWhois package doesn't give us the name information, so we parse the raw information.
    raw_whois = who['raw']

    whois_lines = raw_whois.splitlines()

    # for now, just naively grab lines that might relate to people. Works well for APNIC whois lookups.
    name_lines = list(filter(lambda l: l.startswith("person:"), whois_lines))

    # Alternatively, use the method below to try to catch more
    # match_indicators = re.compile('|'.join(["person", "name"]), re.IGNORECASE)
    # name_lines = list(filter(lambda l: match_indicators.search(l), whois_lines))
    print(ip)
    print(name_lines)
    name = "unknown"
    # Lines are 'label: info', so discard label and strip whitespace.
    if len(name_lines) > 0:
        name = name_lines[0].rpartition(':')[2].lstrip()
    print(name)
    return name


