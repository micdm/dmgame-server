#!/bin/bash

while true; do
    ./start.py $1 >> /tmp/game-$1.log 2>&1
    sleep 5
done
