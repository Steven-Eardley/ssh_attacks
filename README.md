# ssh_attacks

Monitor ssh attack attempts on an ubuntu server. My introduction to Cottage Labs' tech stack. Runs on Python 3.4 (more or less).

## Configuration
Either run the `install.sh` script in the project root folder, or perform the following steps yourself:

* Install python dependencies with `pip install -e .` from the project root folder.
* Run `git submodule init && git submodule update` to install the submodules.
* Download the GeoIP (GeoLiteCity.dat) database from [here](http://geolite.maxmind.com/download/geoip/database/GeoLiteCity.dat.gz).
Extract it, and place it in a folder named `data` within `src`.
* Make a copy of `portality/settings.py` called `app.cfg` in the `src` directory. here you can customise the app settings.

SSH Attacks uses GeoLite data created by MaxMind, available from [http://www.maxmind.com](http://www.maxmind.com).
