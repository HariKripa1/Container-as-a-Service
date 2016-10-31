#!/bin/bash
instance_name=$1
ip_address=$2
service_name=$3
user=$4
git_url=$5
port_no=$6
image_name="dockertestme/"$user"_"$service_name
path="/Users/kasi-mac/.docker/machine/machines/"$instance_name
docker --tlsverify --tlscacert=$path"/ca.pem" --tlscert=$path"/cert.pem" --tlskey=$path"/key.pem" -H $ip_address":2376" build -t $image_name":latest" $git_url
docker --tlsverify --tlscacert=$path"/ca.pem" --tlscert=$path"/cert.pem" --tlskey=$path"/key.pem" -H $ip_address":2376" push $image_name
docker --tlsverify --tlscacert=$path"/ca.pem" --tlscert=$path"/cert.pem" --tlskey=$path"/key.pem" -H $ip_address":2376" service create --replicas 1 --name $service_name --publish :$port_no $image_name 
echo "Result:"docker --tlsverify --tlscacert=$path"/ca.pem" --tlscert=$path"/cert.pem" --tlskey=$path"/key.pem" -H $ip_address":2376" service inspect $service_name