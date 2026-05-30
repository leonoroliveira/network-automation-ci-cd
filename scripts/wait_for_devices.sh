#!/bin/bash

ENV=$1

echo "Waiting 60s for devices to initialise ..."
sleep 60

for device in clab-aar-lab-r1 clab-aar-lab-r2 clab-aar-lab-r3 clab-aar-lab-r4; do
    echo "Waiting for $device SSH ..."

    until nc -z "$device" 22 2>/dev/null; do
        sleep 5
    done

    echo "$device is ready"
done

echo "All devices are ready"