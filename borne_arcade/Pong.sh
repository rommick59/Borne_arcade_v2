#!/bin/bash
xdotool mousemove 1280 1024
cd projet/Pong
java -cp .:../..:$HOME Main
