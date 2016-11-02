#!/bin/bash
instance_name=$1
ip_address=$2
service_name=$3

path="/home/ubuntu/.docker/machine/machines/dm-"$instance_name
docker --tlsverify --tlscacert=$path"/ca.pem" --tlscert=$path"/cert.pem" --tlskey=$path"/key.pem" -H $ip_address":2376" service rm $service_name
