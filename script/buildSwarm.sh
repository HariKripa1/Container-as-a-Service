#!/bin/bash
DEVSTACK_PATH=~/devstack
cd $DEVSTACK_PATH
echo "entering script"
user_name=$1
password=$2
project_name=$3
inst_no=$4
cluster_id=$5
SECURITY_GROUP_NAME="default"
network_name="network_"$user_name
sub_name="subnet_"$user_name
router_name="router_"$user_name
echo "inside script"
echo $username
echo $password
echo $project_name
echo $inst_no
echo $cluster_id
source openrc $user_name $project_name
export OS_PASSWORD=$password
env|grep OS

#test -f ~/.ssh/$user_name.pub || ssh-keygen -t rsa -N "" -f ~/.ssh/$user_name
nova keypair-add --pub-key ~/.ssh/id_rsa.pub $user_name"key"
nova secgroup-add-rule $SECURITY_GROUP_NAME icmp -1 -1 0.0.0.0/0
nova secgroup-add-rule $SECURITY_GROUP_NAME tcp 22 22 0.0.0.0/0
nova secgroup-add-rule $SECURITY_GROUP_NAME tcp 1 65535 0.0.0.0/0
neutron net-create $network_name
network_id=$(neutron net-list | grep $network_name | awk '{print $2}')
neutron subnet-create --dns-nameserver 8.8.8.8 $network_name 10.0.1.0/24 --name $sub_name
public_net_name="public"
neutron router-create $router_name
neutron router-gateway-set $router_name $public_net_name
neutron router-interface-add $router_name $sub_name
image_id=$(openstack image list | grep ubuntu | awk '{print $2}')
cat > inst-config.txt << END
#cloud-config
hostname: ubun
manage_etc_hosts: true
END
x=1
while [ $x -le $inst_no ]
do
    instance_name=$user_name"-"$cluster_id"-instance-"$(( $x - 1 ))
    if [ $x -eq 1 ] 
	then
        instance_name=$user_name"-"$cluster_id"-master"
    fi
    nova boot --flavor d1 --image $image_id --user-data inst-config.txt --nic net-id=$network_id --security-group default --key-name $user_name"key" $instance_name
    nova_id=$(nova list | grep $instance_name| awk '{print $2}')
    floating_ip=$(nova floating-ip-create $public_net_name | grep $public_net_name |awk '{print $4}')
    echo $floating_ip
    sleep 30s
    nova floating-ip-associate $instance_name $floating_ip
    echo "Machine-Information:"$instance_name":"$floating_ip":"$nova_id
    #ssh-keygen -f "/home/ubuntu/.ssh/known_hosts" -R $floating_ip
    #docker-machine create -d generic --generic-ssh-user ubuntu --generic-ssh-key ~/.ssh/$user_name".pub" --generic-ip-address $floating_ip "dm-"$instance_name
    #docker-machine regenerate-certs "dm-"$instance_name
  x=$(( $x + 1 ))
done
