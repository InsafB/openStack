#!/bin/bash

export LC_ALL=C

sudo apt-get update

if sudo apt -y install python3-pip ; then
    echo "python3-pip installation succeeded"
else
    echo "python3-pip installation failed"
fi

if sudo apt-get -y install python-openstackclient ; then
    echo "openstackclient installation succeeded"
else
    echo "openstackclient installation failed"
fi

if sudo apt-get -y install python-swiftclient ; then
    echo "swiftclient installation succeeded"
else
    echo "swiftclient installation failed"
fi

if sudo apt-get -y install python-neutronclient ; then
    echo "neutronclient installation succeeded"
else
    echo "neutronclient installation failed"
fi

if sudo apt-get -y install python-paramiko ; then
    echo "paramiko installation succeeded"
else
    echo "paramiko installation failed"
fi
