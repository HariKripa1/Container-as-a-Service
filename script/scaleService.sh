#!/bin/bash
instance_name=$1
ip_address=$2
service_name=$3
scale_value=$4

path="/Users/kasi-mac/.docker/machine/machines/"$instance_name
docker --tlsverify --tlscacert=$path"/ca.pem" --tlscert=$path"/cert.pem" --tlskey=$path"/key.pem" -H $ip_address":2376" service scale $service_name'='$(($scale_value))