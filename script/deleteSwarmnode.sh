#!/bin/bash
DEVSTACK_PATH=~/devstack
cd $DEVSTACK_PATH
user_name=$1
password=$2
project_name=$3
instance_name=$4
source openrc $user_name $project_name
export OS_PASSWORD=$password
env|grep OS
docker-machine rm 'dm-'$instance_name --force
nova delete $instance_name
