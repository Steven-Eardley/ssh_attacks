#!/bin/bash

# Activate the virtualenv

# Funky way to produce bold text in a terminal
bold=`tput bold`
normal=`tput sgr0`

env=0
echo -n "${bold}Install script for SSH Attacks.${normal}
Has the virtualenv been activated? (Y/n): "

read response

if [ $response == "n" ] || [ $response == "N" ];
then
    echo "${bold}Activating virtualenv now${normal}"
    source ../bin/activate
    env=1
else
    echo "${bold}OK, I'll trust you. Continuing the installation${normal}"
fi

echo "${bold}Installing Python dependencies${normal}"
pip install -e .

echo "${bold}Installing git submodules${normal}"
git submodule init && git submodule update

if [ ! -e ./app.cfg ];
then
    echo "${bold}Making a copy of the settings file${normal}"
    cp portality/settings.py ./app.cfg
fi

if [ ! -d "data" ];
then
    echo "${bold}Getting GeoLite data${normal}"
    # Create a directory for the data
    mkdir data && cd data

    # Download and extract the Geolite data file
    wget http://geolite.maxmind.com/download/geoip/database/GeoLiteCity.dat.gz
    gunzip GeoLiteCity.dat.gz
fi

# If we activated the virtualenv, deactivate it.
if [ $env == 1 ];
then
    echo "${bold}Deactivating the virtualenv${normal}"
    deactivate
fi

echo "${bold}Installation complete. Check and customise the settings in app.cfg
before running SSH Attacks.${normal}"
