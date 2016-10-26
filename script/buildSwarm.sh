#!/bin/bash
DEVSTACK_PATH=~/devstack
cd $DEVSTACK_PATH

user_name=$1
password=$2
project_name=$3
inst_no=$4
SECURITY_GROUP_NAME="default"
network_name="network_"$user_name
sub_name="subnet_"$user_name
router_name="router_"$user_name
source openrc $user_name $project_name
env|grep OS

test -f ~/.ssh/$user_name.pub || ssh-keygen -t rsa -N "" -f ~/.ssh/$user_name
#nova keypair-add --pub-key ~/.ssh/$user_name.pub $user_name"key"
#nova secgroup-add-rule $SECURITY_GROUP_NAME icmp -1 -1 0.0.0.0/0
#nova secgroup-add-rule $SECURITY_GROUP_NAME tcp 22 22 0.0.0.0/0
#neutron net-create $network_name
network_id=$(neutron net-list | grep $network_name | awk '{print $2}')
#neutron subnet-create $network_name 10.0.1.0/24 --name $sub_name
public_net_name="public"
#neutron router-create $router_name
#neutron router-gateway-set $router_name $public_net_name
#neutron router-interface-add $router_name $sub_name
image_id=$(openstack image list | grep ubuntu | awk '{print $2}')
cat > inst-config.txt << END
#cloud-config
hostname: ubun
manage_etc_hosts: true
END
x=1
while [ $x -le $inst_no ]
do
    nova boot --flavor d1 --image $image_id --user-data inst-config.txt --nic net-id=$network_id --security-group default --key-name $user_name"key" $user_name"-instance-"$x
    nova_id=$(nova list | grep $user_name"-instance-"$x | awk '{print $2}')
    floating_ip=$(nova floating-ip-create $public_net_name | grep $public_net_name |awk '{print $4}')
    echo $floating_ip
    sleep 30s
    nova floating-ip-associate $user_name"-instance-"$x $floating_ip
    #ssh-keygen -f "/home/ubuntu/.ssh/known_hosts" -R $floating_ip
    #docker-machine create -d generic --generic-ssh-user ubuntu --generic-ssh-key ~/.ssh/$user_name".pub" --generic-ip-address $floating_ip "dm-"$user_name"-instance-"$x
    #docker-machine regenerate-certs "dm-"$user_name"-instance-"$x

  x=$(( $x + 1 ))
done