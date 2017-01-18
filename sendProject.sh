#!/bin/bash

ip=$1

scp -r openStack-master ubuntu@$ip:~/

scp ~/.ssh/id_rsa ubuntu@$ip:~/.ssh/

scp ~/.ssh/id_rsa.pub ubuntu@$ip:~/.ssh/

scp openStack-master/config ubuntu@$ip:~/.ssh/



