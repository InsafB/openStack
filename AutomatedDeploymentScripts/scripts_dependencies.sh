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

if [[ ("$serverName" = "ServerB") || ("$serverName" = "ServerP") ]]; then
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

if [[ ("$serverName" = "ServerMaster") ]]; then
    if sudo pip3 install Flask-Mail ; then
        echo "flask-mail installation succeeded"
    else
        echo "flask-mail installation failed"
    fi
    if sudo apt-get -y install python ; then
        echo "python installation succeeded"
    else
        echo "python installation failed"
    fi
    if sudo apt-get -y install python-paramiko ; then
        echo "paramiko installation succeeded"
    else
        echo "paramiko installation failed"
    fi
fi    

if [[ ("$serverName" = "ServerI") || ("$serverName" = "ServerS") ]]; then
    if sudo pip3 install pymysql ; then
        echo "pymysql installation succeeded"
    else
        echo "pymysql installation failed"
    fi
    
    mysql -u root -pothmane -e "create database open_stack;use open_stack;create table users(id int(11) primary key,first_name varchar(255),last_name varchar(255),email varchar(255))"
    mysql -u root -pothmane -e "use open_stack;create table plays(id int(11) primary key,timeplay datetime)"
fi    

if [[ ("$serverName" = "ServerW") ]]; then
    sudo apt-get -y install libmagickwand-dev
    sudo apt-get -y install libmagickcore5-extra 
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
