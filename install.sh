#!/bin/sh

# Activate the virtualenv

env = 0
echo -n "Install script for SSH Attacks.\n
Has the virtualenv been activated? (Y/n): "

read response

if (($response == "n") || ($response == "N"))
then
    echo "Activating virtualenv now"
    source ../bin/activate
    $env = 1
else
    echo "OK, I'll trust you. Continuing the installation"
fi

echo "Installing Python dependencies"
pip install -e .

echo "Installing git submodules"
git submodule init && git submodule update

echo "Making a copy of the settings file"
cp portality/settings.py ./app.cfg

echo "Getting GeoLite data"
# Create a directory for the data
mkdir data && cd data

# Download and extract the Geolite data file
wget http://geolite.maxmind.com/download/geoip/database/GeoLiteCity.dat.gz
gunzip GeoLiteCity.dat.gz

if ($env == 1)
then
    deactivate
fi

echo "Installation complete. Check and customise the settings in app.cfg
before running SSH Attacks."
