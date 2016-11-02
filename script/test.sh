#!/bin/sh
t=$1
t1=$2
t2=#3
echo t","t1","t2
echo "helle"
echo "Machine-Information:Master:192.168.1.1:afmslkgmklgkjsdhg"
echo "Machine-Information:Instance-1:192.168.1.2:jfbjfnassg"
echo "fasjfbjkas;gkkgnklsngsg"
echo "Machine-Information:Instance-2:192.168.1.3:asnfbjasfjasjfbjabfjh"
echo "[
    {
        "ID": "bqvv3ad8d4dktxwaehn2nwqyx",
        "Version": {
            "Index": 26
        },
        "CreatedAt": "2016-11-02T04:40:08.372976752Z",
        "UpdatedAt": "2016-11-02T04:40:08.374904372Z",
        "Spec": {
            "Name": "sad_newton",
            "TaskTemplate": {
                "ContainerSpec": {
                    "Image": "dockertestme/kasi_test_1"
                },
                "Resources": {
                    "Limits": {},
                    "Reservations": {}
                },
                "RestartPolicy": {
                    "Condition": "any",
                    "MaxAttempts": 0
                },
                "Placement": {}
            },
            "Mode": {
                "Replicated": {
                    "Replicas": 1
                }
            },
            "UpdateConfig": {
                "Parallelism": 1,
                "FailureAction": "pause"
            },
            "EndpointSpec": {
                "Mode": "vip",
                "Ports": [
                    {
                        "Protocol": "tcp",
                        "TargetPort": 8080,
                        "PublishedPort": 8080
                    }
                ]
            }
        },
        "Endpoint": {
            "Spec": {
                "Mode": "vip",
                "Ports": [
                    {
                        "Protocol": "tcp",
                        "TargetPort": 8080,
                        "PublishedPort": 8080
                    }
                ]
            },
            "Ports": [
                {
                    "Protocol": "tcp",
                    "TargetPort": 8080,
                    "PublishedPort": 8080
                }
            ],
            "VirtualIPs": [
                {
                    "NetworkID": "54z7ffh5z08xj2w81g990lv29",
                    "Addr": "10.255.0.5/16"
                }
            ]
        },
        "UpdateStatus": {
            "StartedAt": "0001-01-01T00:00:00Z",
            "CompletedAt": "0001-01-01T00:00:00Z"
        }
    }
]"