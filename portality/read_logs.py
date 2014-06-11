__author__ = 'steve'
""" Read all matching log files in specified folder, extracting the contents into a usable model, """

import glob, re
from portality.core import app

# Regular Expression to get the relevant lines. We only want sshd lines like this:
# "Jun  6 20:54:18 Zeus sshd[9709]: Invalid user fitzgibbons from 220.177.198.87"
match_attack = re.compile('sshd.*Invalid')

def get_hostname():
    try:
        hostname = app.config['HOST_NAME']
    except KeyError:
        h = open('/etc/hostname', 'r')
        hostname = h.read()

    return hostname.strip()

def read_logs():
    """
    Read all logs in the directory specified in AUTH_LOGS in app.cfg, or system default.
    :return:
    """
    try:
        path = app.config['AUTH_LOGS']
    except KeyError:
        path = '/var/log'

    for log in glob.glob(path + '/auth*'):
        f = open(log, 'r')
        try:
            [extract_model(line.strip()) for line in f.readlines() if match_attack.search(line)]
        except UnicodeDecodeError:
            print("No invalid user login attempts found. Aborting.")
            exit(0)

def extract_model(log_entry):

    hostname = get_hostname()
    print(log_entry.split(hostname))
    print(log_entry)

read_logs()