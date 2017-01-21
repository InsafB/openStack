#!/bin/bash

ip=$1
rsa_priv=$2
rsa_pub=$3

scp -r openStack-master ubuntu@$ip:~/

scp $rsa_priv ubuntu@$ip:~/.ssh/

scp $rsa_pub ubuntu@$ip:~/.ssh/

scp openStack-master/config ubuntu@$ip:~/.ssh/
