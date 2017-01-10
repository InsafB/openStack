#!/bin/sh

export LC_ALL=C

sudo apt-get update

sudo apt -y install python3-pip

sudo apt-get -y install python-openstackclient
sudo apt-get -y install python-swiftclient 
sudo apt-get -y install python-neutronclient

sudo pip3 install flask
sudo apt-get -y install python-mysqldb
