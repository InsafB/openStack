#!/bin/bash

serverName=$1
sourcefile=$2

source ~/openStack-master/$sourcefile

export LC_ALL=C

sudo apt-get update

if sudo apt -y install python3-pip ; then
    echo "python3-pip installation succeeded"
else
    echo "python3-pip installation failed"
fi

if [[ ("$serverName" = "ServerB") || ("$serverName" = "ServerP") ]] then
    if sudo apt-get -y install python3-swiftclient ; then
        echo "swiftclient installation succeeded"
    else
        echo "swiftclient installation failed"
    fi
fi   

if sudo pip3 install flask ; then
    echo "flask installation succeeded"
else
    echo "flask installation failed"
fi

if [[ ("$serverName" = "ServerMaster") ]] then
    if sudo pip3 install Flask-Mail ; then
        echo "flask-mail installation succeeded"
    else
        echo "flask-mail installation failed"
    fi
fi    

if [[ ("$serverName" = "ServerB") || ("$serverName" = "ServerP") ]] then
    if sudo pip3 install pymysql ; then
        echo "pymysql installation succeeded"
    else
        echo "pymysql installation failed"
    fi
fi    

if [[ ("$serverName" = "ServerW") ]] then
    sudo apt-get install libmagickwand-dev
    sudo apt-get install libmagickcore5-extra 
    wget http://www.imagemagick.org/download/ImageMagick.tar.gz
    tar -xvf ImageMagick.tar.gz
    cd ImageMagick-7.* 
    ./configure 
    make
    if sudo make install ; then
        sudo ldconfig /usr/local/lib
        echo "MagikImage installation succeeded"
    else
        echo "MagikImage installation failed"
    fi
fi
