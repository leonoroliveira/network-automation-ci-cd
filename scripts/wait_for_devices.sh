#!/bin/bash

ENV=$1

if [ "$ENV" = "twin" ]; then
    PREFIX="clab-aar-lab-twin"
else
    PREFIX="clab-aar-lab"
fi

echo "Waiting 60s for devices to initialise ..."
sleep 60

for device in "$PREFIX-r1" "$PREFIX-r2" "$PREFIX-r3" "$PREFIX-r4"; do
    echo "Waiting for $device SSH ..."

    until nc -z "$device" 22 2>/dev/null; do
        sleep 5
    done

    echo "$device is ready"
done

echo "All devices are ready"