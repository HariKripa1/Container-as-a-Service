#!/bin/bash
DEVSTACK_PATH=~/devstack
cd $DEVSTACK_PATH
user_name=$1
password=$2
project_name=$3
floating_ip=$4
instance_name=$5
source openrc $user_name $project_name
env|grep OS
x=1
ssh-keygen -f "/home/ubuntu/.ssh/known_hosts" -R $floating_ip
while [ $x -le 200 ]
do
    if ssh $floating_ip 'exit'; then
        #echo "success"
        break
    else
        sleep 10s
    fi
    x=$(( $x + 1 ))
done
if [ $x -eq 500 ]
then
    echo "failure"
else
    echo "success"
    docker-machine create -d generic --generic-ssh-user ubuntu --generic-ssh-key ~/.ssh/id_rsa.pub --generic-ip-address $floating_ip "dm-"$instance_name
    #docker-machine regenerate-certs "dm-"$instance_name
fi
