#!/bin/bash
DEVSTACK_PATH=~/devstack
cd $DEVSTACK_PATH
source openrc admin admin
user_name=$1
password=$2
project_name="project_"$1

openstack user create --password $password $user_name
openstack project create --description $user_name" Project" $project_name
openstack role create user
openstack role add --project $project_name --user $user_name user

echo "Project and User Successfully Create"