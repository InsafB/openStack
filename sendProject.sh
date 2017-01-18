#!/bin/bash

ip=$1
rsa_priv=$2
rsa_pub=$3

scp -r openStack-master ubuntu@$ip:~/

scp ~/.ssh/id_rsa ubuntu@$rsa_priv:~/.ssh/

scp ~/.ssh/id_rsa.pub ubuntu@$rsa_pub:~/.ssh/

scp openStack-master/config ubuntu@$ip:~/.ssh/
