#!/bin/sh

# Activate the virtualenv
source ../bin/activate

# Install python dependencies
pip install -e .

# Install git submodules
git submodule init && git submodule update

# Make a copy of the settings file
cp portality/settings.py ./app.cfg

# Create a directory for the data
mkdir data && cd data

# Download and extract the Geolite data file
wget http://geolite.maxmind.com/download/geoip/database/GeoLiteCity.dat.gz
gunzip GeoLiteCity.dat.gz

deactivate

echo "Installation complate. Check and customise the settings in app.cfg
before running SSH Attacks."