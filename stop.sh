#!/bin/bash

function kill_daemon {
    pkill -f "/bin/bash ./loop.sh $1"
    pkill -f "../bin/python ./start.py $1"
}

kill_daemon policy
kill_daemon web
kill_daemon ws
