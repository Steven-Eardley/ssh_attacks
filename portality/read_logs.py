__author__ = 'steve'
""" Read all matching log files in specified folder, extracting the contents into a usable model, """

import glob, re
from portality.core import app
from portality import models
from datetime import datetime

# Regular Expressions to get the relevant lines. We only want sshd lines like this:
# "Jun  6 20:54:18 Zeus sshd[9709]: Invalid user fitzgibbons from 220.177.198.87"
match_attack = re.compile('sshd.*Invalid')
match_event_no = re.compile('[\d*]')

# Count the total number of log lines inserted in the index.
line_count = 0

# Return configured hostname, or get the one from the current machine.
def get_hostname():
    try:
        hostname = app.config['HOST_NAME']
    except KeyError:
        h = open('/etc/hostname', 'r')
        hostname = h.read()

    return hostname.strip()

#TODO: handle archives (currently requires the logs to have been manually extracted.
def read_logs():
    """
    Read all logs in the directory specified in AUTH_LOGS in app.cfg, or system default.
    :return:
    """

    # Count number of files processed
    file_count = 0

    # If the user has configured a path, use that. Else use standard system directory
    try:
        path = app.config['AUTH_LOGS']
    except KeyError:
        path = '/var/log'

    # Read all auth.log files in the provided path
    for log in glob.glob(path + '/auth*'):
        f = open(log, 'r')
        try:
            [extract_model(line.strip()) for line in f.readlines() if match_attack.search(line)]
            file_count += 1
        except UnicodeDecodeError:
            print("No invalid user login attempts found. Aborting.")
            exit(0)

    global line_count
    print("{0} log entries successfully imported from {1} files.".format(line_count, file_count))

#TODO: year isn't in logs so we set the current year, This may not always be true.
def extract_model(log_entry):
    # Split on the machine's hostname to separate the time from the details
    hostname = get_hostname()
    [time, details] = log_entry.split(hostname)
    attack_time = datetime.strptime(time, '%b  %d %H:%M:%S ')
    attack_time = attack_time.replace(year=datetime.now().year)
    attack_event_no = ''.join(match_event_no.findall(details.split()[0]))
    attack_user = details.split()[3]
    attack_ip = details.split()[5]

    # Use the event number + time as the ID, so we avoid adding duplicates to the index
    id_str = attack_event_no+'D'+attack_time.isoformat()

    # Put this in an ssh_entry DomainObject, and save to the index
    attack_model = models.SshEntry(id=id_str)
    attack_model.set_attack_time(str(attack_time))
    attack_model.set_attack_name(attack_user)
    attack_model.set_attack_ip(attack_ip)
    attack_model.save()

    # Increment our processed entry count
    global line_count
    line_count += 1

if __name__ == "__main__":
    read_logs()